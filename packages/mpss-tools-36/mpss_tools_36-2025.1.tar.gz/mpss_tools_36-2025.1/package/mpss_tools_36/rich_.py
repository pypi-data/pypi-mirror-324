import typing as h
from multiprocessing import Manager as NewSharingManager
from multiprocessing.managers import DictProxy as shared_dict_t
from multiprocessing.managers import SyncManager as sharing_manager_t

from rich.progress import Progress as base_t
from rich.progress import Task as task_t
from rich.progress import TaskID as task_id_t
from rich.progress import TimeRemainingColumn as column_eta_t

status_per_task_h = shared_dict_t[task_id_t, int | float]


class progress_t(base_t):
    """
    Incompatible with the dataclass extension.
    """

    sharing_manager: sharing_manager_t | None = None
    status_per_task: status_per_task_h | None = None
    global_task: task_t | None = None

    @classmethod
    def New(
        cls,
        *args,
        refresh_per_second: int | float = 1.0,
        speed_estimate_period: int | float = 10.0,
        elapsed_when_finished: bool = True,
        for_several_processes: bool = False,
        with_overall_progress: str | None = "Overall",
        **kwargs,
    ) -> h.Self:
        """"""
        if args.__len__() > 0:
            columns = args
        else:
            columns = base_t.get_default_columns()
            if elapsed_when_finished:
                columns = columns[:-1] + (column_eta_t(elapsed_when_finished=True),)

        output = cls(
            *columns,
            refresh_per_second=refresh_per_second,
            speed_estimate_period=speed_estimate_period,
            **kwargs,
        )

        if for_several_processes:
            output.sharing_manager = NewSharingManager()
            output.status_per_task = output.sharing_manager.dict()
            if with_overall_progress is not None:
                task_id = output.add_task(with_overall_progress.upper(), total=0.0)
                output.global_task = output.tasks[task_id]

        return output

    def NewTask(self, *args, **kwargs) -> task_id_t:
        """"""
        output = self.add_task(*args, **kwargs)

        if self.status_per_task is not None:
            self.status_per_task[output] = 0.0
            if self.global_task is not None:
                self.global_task.total += self.tasks[output].total

        return output

    @staticmethod
    def Update(
        progress: base_t | None,
        status_per_task: status_per_task_h | None,
        task_id: task_id_t,
        completed: int | float,
        /,
    ) -> None:
        """"""
        if status_per_task is None:
            progress.update(task_id, completed=completed)
        else:
            status_per_task[task_id] = completed

    def TrackUpdates(self) -> None:
        """"""
        assert self.status_per_task is not None

        status_per_task = self.status_per_task
        global_task = self.global_task

        while not self.finished:
            completed_global = 0.0
            for task_id, completed in status_per_task.items():
                # task_id cannot be global_task.id.
                self.update(task_id, completed=completed)

                completed_global += completed

            if global_task is not None:
                # min: For round-off errors.
                completed_global = min(completed_global, global_task.total)
                self.update(global_task.id, completed=completed_global)

    def PrintAbove(self, *args, **kwargs) -> None:
        """"""
        self.console.print(*args, **kwargs)

    def __del__(self) -> None:
        """"""
        if self.sharing_manager is not None:
            self.sharing_manager.shutdown()
