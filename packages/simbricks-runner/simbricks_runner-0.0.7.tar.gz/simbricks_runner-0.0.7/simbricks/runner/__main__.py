# Copyright 2024 Max Planck Institute for Software Systems, and
# National University of Singapore
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from __future__ import annotations

import asyncio
import datetime
import json
import logging
import pathlib
import traceback
import typing
import uuid

from simbricks import client
from simbricks.orchestration.instantiation import base as inst_base
from simbricks.orchestration.simulation import base as sim_base
from simbricks.orchestration.system import base as sys_base
from simbricks.runner import settings
from simbricks.runtime import simulation_executor as sim_exec
from simbricks.utils import artifatcs as art
from simbricks.schemas import base as schemas

if typing.TYPE_CHECKING:
    from simbricks.orchestration.instantiation import proxy as inst_proxy


class RunnerSimulationExecutorCallbacks(sim_exec.SimulationExecutorCallbacks):

    def __init__(
        self,
        instantiation: inst_base.Instantiation,
        rc: client.RunnerClient,
        run_id: int,
    ):
        super().__init__(instantiation)
        self._instantiation = instantiation
        self._client: client.RunnerClient = rc
        self._run_id: int = run_id
        self._active_simulator_cmd: dict[sim_base.Simulator, str] = {}
        self._active_proxy_cmd: dict[inst_proxy.Proxy, str] = {}

    # ---------------------------------------
    # Callbacks related to whole simulation -
    # ---------------------------------------

    async def simulation_prepare_cmd_start(self, cmd: str) -> None:
        LOGGER.debug(f"+ [prepare] {cmd}")
        # TODO (Jonas) Send executed prepare command to backend

    async def simulation_prepare_cmd_stdout(self, cmd: str, lines: list[str]) -> None:
        super().simulation_prepare_cmd_stdout(cmd, lines)
        for line in lines:
            LOGGER.debug(f"[prepare] {line}")
        await self._client.send_out_simulation(self._run_id, cmd, False, lines)

    async def simulation_prepare_cmd_stderr(self, cmd: str, lines: list[str]) -> None:
        super().simulation_prepare_cmd_stderr(cmd, lines)
        for line in lines:
            LOGGER.debug(f"[prepare] {line}")
        await self._client.send_out_simulation(self._run_id, cmd, True, lines)

    # -----------------------------
    # Simulator-related callbacks -
    # -----------------------------

    async def simulator_prepare_started(self, sim: sim_base.Simulator, cmd: str) -> None:
        self._active_simulator_cmd[sim] = cmd
        LOGGER.debug(f"+ [{sim.full_name()}] {cmd}")
        await self._client.update_state_simulator(
            self._run_id, sim.id(), sim.full_name(), "preparing", cmd
        )

    async def simulator_prepare_exited(self, sim: sim_base.Simulator, exit_code: int) -> None:
        self._active_simulator_cmd.pop(sim)
        LOGGER.debug(f"- [{sim.full_name()}] exited with code {exit_code}")
        # TODO (Jonas) Report to backend if prepare command fails

    async def simulator_prepare_stdout(self, sim: sim_base.Simulator, lines: list[str]) -> None:
        for line in lines:
            LOGGER.debug(f"[{sim.full_name()}] {line}")
        await self._client.send_out_simulator(
            self._run_id, sim.id(), sim.full_name(), False, lines, datetime.datetime.now()
        )

    async def simulator_prepare_stderr(self, sim: sim_base.Simulator, lines: list[str]) -> None:
        for line in lines:
            LOGGER.debug(f"[{sim.full_name()}] {line}")
        await self._client.send_out_simulator(
            self._run_id, sim.id(), sim.full_name(), True, lines, datetime.datetime.now()
        )

    async def simulator_started(self, sim: sim_base.Simulator, cmd: str) -> None:
        self._active_simulator_cmd[sim] = cmd
        LOGGER.debug(f"+ [{sim.full_name()}] {cmd}")
        await self._client.update_state_simulator(
            self._run_id, sim.id(), sim.full_name(), "starting", cmd
        )

    async def simulator_ready(self, sim: sim_base.Simulator) -> None:
        LOGGER.debug(f"[{sim.full_name()}] has started successfully")
        # NOTE: this can happen due to coroutine scheduling and the termination of simulators
        if sim not in self._active_simulator_cmd:
            LOGGER.warning(
                f"cannot mark simulator as ready as it was already removed: {sim.full_name()}"
            )
            return
        await self._client.update_state_simulator(
            self._run_id, sim.id(), sim.full_name(), "running", self._active_simulator_cmd[sim]
        )

    async def simulator_exited(self, sim: sim_base.Simulator, exit_code: int) -> None:
        cmd = self._active_simulator_cmd.pop(sim)
        LOGGER.debug(f"- [{sim.full_name()}] exited with code {exit_code}")
        await self._client.update_state_simulator(
            self._run_id, sim.id(), sim.full_name(), "terminated", cmd
        )

    async def simulator_stdout(self, sim: sim_base.Simulator, lines: list[str]) -> None:
        for line in lines:
            LOGGER.debug(f"[{sim.full_name()}] {line}")
        await self._client.send_out_simulator(
            self._run_id, sim.id(), sim.full_name(), False, lines, datetime.datetime.now()
        )

    async def simulator_stderr(self, sim: sim_base.Simulator, lines: list[str]) -> None:
        for line in lines:
            LOGGER.debug(f"[{sim.full_name()}] {line}")
        await self._client.send_out_simulator(
            self._run_id, sim.id(), sim.full_name(), True, lines, datetime.datetime.now()
        )

    # -------------------------
    # Proxy-related callbacks -
    # -------------------------

    async def proxy_started(self, proxy: inst_proxy.Proxy, cmd: str) -> None:
        self._active_proxy_cmd[proxy] = cmd
        LOGGER.debug(f"+ [{proxy.name}] {cmd}")
        await self._client.update_state_proxy(self._run_id, proxy.id(), "starting", cmd)

    async def proxy_ready(self, proxy: inst_proxy.Proxy) -> None:
        LOGGER.debug(f"[{proxy.name}] has started successfully")
        await self._client.update_state_proxy(
            self._run_id, proxy.id(), "running", self._active_proxy_cmd[proxy]
        )

    async def proxy_exited(self, proxy: inst_proxy.Proxy, exit_code: int) -> None:
        cmd = self._active_proxy_cmd.pop(proxy)
        LOGGER.debug(f"- [{proxy.name}] exited with code {exit_code}")
        await self._client.update_state_proxy(self._run_id, proxy.id(), "terminated", cmd)

    async def proxy_stdout(self, proxy: inst_proxy.Proxy, lines: list[str]) -> None:
        for line in lines:
            LOGGER.debug(f"[{proxy.name}] {line}")
        await self._client.send_out_proxy(self._run_id, proxy.id(), False, lines)

    async def proxy_stderr(self, proxy: inst_proxy.Proxy, lines: list[str]) -> None:
        for line in lines:
            LOGGER.debug(f"[{proxy.name}] {line}")
        await self._client.send_out_proxy(self._run_id, proxy.id(), True, lines)


class Run:
    def __init__(
        self,
        run_id: int,
        inst: inst_base.Instantiation,
        callbacks: RunnerSimulationExecutorCallbacks,
        runner: sim_exec.SimulationExecutor,
    ) -> None:
        self.run_id: int = run_id
        self.inst: inst_base.Instantiation = inst
        self.callbacks: RunnerSimulationExecutorCallbacks = callbacks
        self.cancelled: bool = False
        self.runner: sim_exec.SimulationExecutor = runner
        self.exec_task: asyncio.Task | None = None


class Runner:

    def __init__(
        self, base_url: str, workdir: str, namespace: str, ident: int, polling_delay_sec: int
    ):
        self._base_url: str = base_url
        self._workdir: pathlib.Path = pathlib.Path(workdir).resolve()
        self._polling_delay_sec: int = polling_delay_sec
        self._namespace: str = namespace
        self._ident: int = ident
        self._base_client = client.BaseClient(base_url=base_url)
        self._namespace_client = client.NSClient(base_client=self._base_client, namespace=namespace)
        self._sb_client = client.SimBricksClient(self._namespace_client)
        self._rc = client.RunnerClient(self._namespace_client, ident)

        # self._cur_run: Run | None = None  # currently executed run
        # self._to_run_queue: asyncio.Queue = asyncio.Queue()  # queue of run ids to run next
        self._run_map: dict[int, Run] = {}

    async def _fetch_assemble_inst(self, run_id: int) -> inst_base.Instantiation:
        LOGGER.debug(f"fetch and assemble instantiation related to run {run_id}")

        run_obj_list = await self._rc.filter_get_runs(run_id=run_id, state="pending")
        if not run_obj_list or len(run_obj_list) != 1:
            msg = f"could not fetch run with id {run_id} that is still 'pending'"
            LOGGER.error(msg)
            raise Exception(msg)
        run_obj = run_obj_list[0]

        run_workdir = self._workdir / f"run-{run_id}"
        if run_workdir.exists():
            LOGGER.warning(
                f"the directory {run_workdir} already exists, will create a new one using a uuid"
            )
            run_workdir = self._workdir / f"run-{run_id}-{str(uuid.uuid4())}"
        run_workdir.mkdir(parents=True)

        assert run_obj.instantiation_id
        inst_obj = await self._sb_client.get_instantiation(run_obj.instantiation_id)
        assert inst_obj.simulation_id
        sim_obj = await self._sb_client.get_simulation(inst_obj.simulation_id)
        assert sim_obj.system_id
        sys_obj = await self._sb_client.get_system(sim_obj.system_id)

        system = sys_base.System.fromJSON(json.loads(sys_obj.sb_json))
        simulation = sim_base.Simulation.fromJSON(system, json.loads(sim_obj.sb_json))
        tmp_inst = inst_base.Instantiation.fromJSON(simulation, json.loads(inst_obj.sb_json))

        env = inst_base.InstantiationEnvironment(workdir=run_workdir)  # TODO
        inst = inst_base.Instantiation(sim=simulation)
        inst.env = env
        inst.preserve_tmp_folder = tmp_inst.preserve_tmp_folder
        inst.create_checkpoint = tmp_inst.create_checkpoint
        inst.artifact_name = tmp_inst.artifact_name
        inst.artifact_paths = tmp_inst.artifact_paths
        return inst

    async def _prepare_run(self, run_id: int) -> Run:
        LOGGER.debug(f"prepare run {run_id}")

        inst = await self._fetch_assemble_inst(run_id=run_id)
        callbacks = RunnerSimulationExecutorCallbacks(inst, self._rc, run_id)
        runner = sim_exec.SimulationExecutor(inst, callbacks, settings.RunnerSettings().verbose)
        await runner.prepare()

        run = Run(run_id=run_id, inst=inst, runner=runner, callbacks=callbacks)
        return run

    async def _start_run(self, run: Run) -> None:
        sim_task: asyncio.Task | None = None
        try:
            LOGGER.info(f"start run {run.run_id}")

            await self._rc.update_run(run.run_id, schemas.RunState.RUNNING, "")

            # TODO: allow for proper checkpointing run
            sim_task = asyncio.create_task(run.runner.run())
            res = await sim_task

            output_path = run.inst.get_simulation_output_path()
            res.dump(outpath=output_path)  # TODO: FIXME
            if run.inst.create_artifact:
                art.create_artifact(
                    artifact_name=run.inst.artifact_name,
                    paths_to_include=run.inst.artifact_paths,
                )
                await self._sb_client.set_run_artifact(run.run_id, run.inst.artifact_name)

            status = schemas.RunState.ERROR if res.failed() else schemas.RunState.COMPLETED
            await self._rc.update_run(run.run_id, status, output="")

            await run.runner.cleanup()

            LOGGER.info(f"finished run {run.run_id}")

        except asyncio.CancelledError:
            LOGGER.debug("_start_sim handel cancelled error")
            if sim_task:
                sim_task.cancel()
            await self._rc.update_run(run.run_id, state=schemas.RunState.CANCELLED, output="")
            LOGGER.info(f"cancelled execution of run {run.run_id}")

        except Exception as ex:
            LOGGER.debug("_start_sim handel error")
            if sim_task:
                sim_task.cancel()
            await self._rc.update_run(run_id=run.run_id, state=schemas.RunState.ERROR, output="")
            LOGGER.error(f"error while executing run {run.run_id}: {ex}")

    async def _cancel_all_tasks(self) -> None:
        for _, run in self._run_map.items():
            if run.exec_task.done():
                continue

            run.exec_task.cancel()
            await run.exec_task

    async def _handel_events(self) -> None:
        try:
            await self._rc.runner_started()

            while True:
                # fetch all events not handeled yet
                events = list(
                    await self._rc.get_events(
                        run_id=None,
                        action=None,
                        limit=None,
                        event_status=schemas.RunnerEventStatus.PENDING,
                    )
                )
                for run_id in list(self._run_map.keys()):
                    run = self._run_map[run_id]
                    # check if run finished and cleanup map
                    if run.exec_task and run.exec_task.done():
                        run = self._run_map.pop(run_id)
                        LOGGER.debug(f"removed run {run_id} from run_map")
                        assert run_id not in self._run_map
                        continue
                    # only fecth events in case run is not finished yet
                    run_events = list(
                        await self._rc.get_events(
                            run_id=run_id,
                            action=None,
                            limit=None,
                            event_status=schemas.RunnerEventStatus.PENDING,
                        )
                    )
                    events.extend(run_events)

                LOGGER.debug(f"events fetched ({len(events)}): {events}")

                # handel the fetched events
                for event in events:
                    event_id = event.id
                    run_id = event.run_id if event.run_id else None
                    LOGGER.debug(f"try to handel event {event}")

                    event_status = schemas.RunnerEventStatus.COMPLETED
                    match event.action:
                        case schemas.RunnerEventAction.KILL:
                            if run_id and not run_id in self._run_map:
                                event_status = schemas.RunnerEventStatus.CANCELLED
                            else:
                                run = self._run_map[run_id]
                                run.exec_task.cancel()
                                await run.exec_task
                                LOGGER.debug(f"executed kill to cancel execution of run {run_id}")
                        case schemas.RunnerEventAction.HEARTBEAT:
                            await self._rc.send_heartbeat()
                            LOGGER.debug(f"send heartbeat")
                        case schemas.RunnerEventAction.START_RUN:
                            if not run_id or run_id in self._run_map:
                                LOGGER.debug(
                                    f"cannot start run, no run id or run with given id is being executed"
                                )
                                event_status = schemas.RunnerEventStatus.CANCELLED
                            else:
                                try:
                                    run = await self._prepare_run(run_id=run_id)
                                    run.exec_task = asyncio.create_task(self._start_run(run=run))
                                    self._run_map[run_id] = run
                                    LOGGER.debug(f"started execution of run {run_id}")
                                except Exception as err:
                                    LOGGER.error(f"could not prepare run {run_id}: {err}")
                                    await self._rc.update_run(run_id, schemas.RunState.ERROR, "")
                                    event_status = schemas.RunnerEventStatus.CANCELLED
                        case schemas.RunnerEventAction.SIMULATION_STATUS:
                            if not run_id or not run_id in self._run_map:
                                event_status = schemas.RunnerEventStatus.CANCELLED
                            else:
                                run = self._run_map[run_id]
                                await run.runner.sigusr1()
                                LOGGER.debug(f"send sigusr1 to run {run_id}")

                    await self._rc.update_runner_event(
                        event_id=event_id, event_status=event_status, action=None, run_id=None
                    )
                    LOGGER.info(f"handeled event {event_id}")

                await asyncio.sleep(self._polling_delay_sec)

        except asyncio.CancelledError:
            LOGGER.error(f"cancelled event handling loop")
            await self._cancel_all_tasks()

        except Exception:
            await self._cancel_all_tasks()
            trace = traceback.format_exc()
            LOGGER.error(f"an error occured while running: {trace}")

    async def run(self) -> None:
        LOGGER.info("STARTED RUNNER")
        LOGGER.debug(
            f" runner params: base_url={self._base_url}, workdir={self._workdir}, namespace={self._namespace}, ident={self._ident}, polling_delay_sec={self._polling_delay_sec}"
        )

        try:
            await self._handel_events()
        except Exception as exc:
            LOGGER.error(f"fatal error {exc}")
            raise exc

        LOGGER.info("TERMINATED RUNNER")


async def amain():
    runner = Runner(
        base_url=settings.runner_settings().base_url,
        workdir=pathlib.Path("./runner-work").resolve(),
        namespace=settings.runner_settings().namespace,
        ident=settings.runner_settings().runner_id,
        polling_delay_sec=settings.runner_settings().polling_delay_sec,
    )

    await runner.run()


def setup_logger() -> logging.Logger:
    level = settings.RunnerSettings().log_level
    logging.basicConfig(
        level=level, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger(__name__)
    return logger


LOGGER = setup_logger()


def main():
    asyncio.run(amain())


if __name__ == "__main__":
    main()
