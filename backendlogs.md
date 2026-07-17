request_id=fcaf097c status_code=200
2026-03-22 01:46:32 INFO:     192.168.65.1:47298 - "GET /api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed HTTP/1.1" 200 OK
2026-03-22 01:46:32 2026-03-21 20:16:32,902 INFO sqlalchemy.engine.Engine COMMIT
2026-03-22 01:46:35 2026-03-21T20:16:35.870342Z [info     ] request_started                method=GET path=/api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed request_id=b80dafc1
2026-03-22 01:46:35 2026-03-21 20:16:35,886 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-03-22 01:46:35 2026-03-21 20:16:35,886 INFO sqlalchemy.engine.Engine SELECT users.username, users.hashed_password, users.is_active, users.id, users.created_at, users.updated_at 
2026-03-22 01:46:35 FROM users 
2026-03-22 01:46:35 WHERE users.id = $1::UUID
2026-03-22 01:46:35 2026-03-21 20:16:35,886 INFO sqlalchemy.engine.Engine [cached since 3648s ago] (UUID('65f5b699-1b79-4510-8206-85c128fb87e1'),)
2026-03-22 01:46:35 2026-03-21 20:16:35,900 INFO sqlalchemy.engine.Engine SELECT scan_jobs.status, scan_jobs.job_type, scan_jobs.total, scan_jobs.processed, scan_jobs.error, scan_jobs.started_at, scan_jobs.completed_at, scan_jobs.created_at, scan_jobs.id 
2026-03-22 01:46:35 FROM scan_jobs 
2026-03-22 01:46:35 WHERE scan_jobs.id = $1::UUID
2026-03-22 01:46:35 2026-03-21 20:16:35,900 INFO sqlalchemy.engine.Engine [cached since 1735s ago] (UUID('d38b864e-3938-40ef-8c27-7b2df093cbed'),)
2026-03-22 01:46:35 2026-03-21T20:16:35.901066Z [info     ] request_completed              duration_ms=30.79 method=GET path=/api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed request_id=b80dafc1 status_code=200
2026-03-22 01:46:35 INFO:     192.168.65.1:47298 - "GET /api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed HTTP/1.1" 200 OK
2026-03-22 01:46:35 2026-03-21 20:16:35,901 INFO sqlalchemy.engine.Engine COMMIT
2026-03-22 01:46:38 2026-03-21T20:16:38.867349Z [info     ] request_started                method=GET path=/api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed request_id=ec621ce4
2026-03-22 01:46:38 2026-03-21 20:16:38,879 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-03-22 01:46:38 2026-03-21 20:16:38,881 INFO sqlalchemy.engine.Engine SELECT users.username, users.hashed_password, users.is_active, users.id, users.created_at, users.updated_at 
2026-03-22 01:46:38 FROM users 
2026-03-22 01:46:38 WHERE users.id = $1::UUID
2026-03-22 01:46:38 2026-03-21 20:16:38,881 INFO sqlalchemy.engine.Engine [cached since 3651s ago] (UUID('65f5b699-1b79-4510-8206-85c128fb87e1'),)
2026-03-22 01:46:38 2026-03-21 20:16:38,889 INFO sqlalchemy.engine.Engine SELECT scan_jobs.status, scan_jobs.job_type, scan_jobs.total, scan_jobs.processed, scan_jobs.error, scan_jobs.started_at, scan_jobs.completed_at, scan_jobs.created_at, scan_jobs.id 
2026-03-22 01:46:38 FROM scan_jobs 
2026-03-22 01:46:38 WHERE scan_jobs.id = $1::UUID
2026-03-22 01:46:38 2026-03-21 20:16:38,889 INFO sqlalchemy.engine.Engine [cached since 1738s ago] (UUID('d38b864e-3938-40ef-8c27-7b2df093cbed'),)
2026-03-22 01:46:38 2026-03-21T20:16:38.892231Z [info     ] request_completed              duration_ms=24.89 method=GET path=/api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed request_id=ec621ce4 status_code=200
2026-03-22 01:46:38 INFO:     192.168.65.1:47298 - "GET /api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed HTTP/1.1" 200 OK
2026-03-22 01:46:38 2026-03-21 20:16:38,899 INFO sqlalchemy.engine.Engine COMMIT
2026-03-22 01:46:41 2026-03-21T20:16:41.866865Z [info     ] request_started                method=GET path=/api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed request_id=c2764e74
2026-03-22 01:46:41 2026-03-21 20:16:41,877 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-03-22 01:46:41 2026-03-21 20:16:41,878 INFO sqlalchemy.engine.Engine SELECT users.username, users.hashed_password, users.is_active, users.id, users.created_at, users.updated_at 
2026-03-22 01:46:41 FROM users 
2026-03-22 01:46:41 WHERE users.id = $1::UUID
2026-03-22 01:46:41 2026-03-21 20:16:41,878 INFO sqlalchemy.engine.Engine [cached since 3654s ago] (UUID('65f5b699-1b79-4510-8206-85c128fb87e1'),)
2026-03-22 01:46:41 2026-03-21 20:16:41,887 INFO sqlalchemy.engine.Engine SELECT scan_jobs.status, scan_jobs.job_type, scan_jobs.total, scan_jobs.processed, scan_jobs.error, scan_jobs.started_at, scan_jobs.completed_at, scan_jobs.created_at, scan_jobs.id 
2026-03-22 01:46:41 FROM scan_jobs 
2026-03-22 01:46:41 WHERE scan_jobs.id = $1::UUID
2026-03-22 01:46:41 2026-03-21 20:16:41,887 INFO sqlalchemy.engine.Engine [cached since 1741s ago] (UUID('d38b864e-3938-40ef-8c27-7b2df093cbed'),)
2026-03-22 01:46:41 2026-03-21T20:16:41.890855Z [info     ] request_completed              duration_ms=24.03 method=GET path=/api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed request_id=c2764e74 status_code=200
2026-03-22 01:46:41 INFO:     192.168.65.1:47298 - "GET /api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed HTTP/1.1" 200 OK
2026-03-22 01:46:41 2026-03-21 20:16:41,891 INFO sqlalchemy.engine.Engine COMMIT
2026-03-22 01:46:44 2026-03-21T20:16:44.868920Z [info     ] request_started                method=GET path=/api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed request_id=694544a3
2026-03-22 01:46:44 2026-03-21 20:16:44,889 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-03-22 01:46:44 2026-03-21 20:16:44,890 INFO sqlalchemy.engine.Engine SELECT users.username, users.hashed_password, users.is_active, users.id, users.created_at, users.updated_at 
2026-03-22 01:46:44 FROM users 
2026-03-22 01:46:44 WHERE users.id = $1::UUID
2026-03-22 01:46:44 2026-03-21 20:16:44,891 INFO sqlalchemy.engine.Engine [cached since 3657s ago] (UUID('65f5b699-1b79-4510-8206-85c128fb87e1'),)
2026-03-22 01:46:44 2026-03-21 20:16:44,895 INFO sqlalchemy.engine.Engine SELECT scan_jobs.status, scan_jobs.job_type, scan_jobs.total, scan_jobs.processed, scan_jobs.error, scan_jobs.started_at, scan_jobs.completed_at, scan_jobs.created_at, scan_jobs.id 
2026-03-22 01:46:44 FROM scan_jobs 
2026-03-22 01:46:44 WHERE scan_jobs.id = $1::UUID
2026-03-22 01:46:44 2026-03-21 20:16:44,895 INFO sqlalchemy.engine.Engine [cached since 1744s ago] (UUID('d38b864e-3938-40ef-8c27-7b2df093cbed'),)
2026-03-22 01:46:44 2026-03-21T20:16:44.901487Z [info     ] request_completed              duration_ms=32.62 method=GET path=/api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed request_id=694544a3 status_code=200
2026-03-22 01:46:44 INFO:     192.168.65.1:47298 - "GET /api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed HTTP/1.1" 200 OK
2026-03-22 01:46:44 2026-03-21 20:16:44,902 INFO sqlalchemy.engine.Engine COMMIT
2026-03-22 01:46:47 2026-03-21T20:16:47.871426Z [info     ] request_started                method=GET path=/api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed request_id=e71642e1
2026-03-22 01:46:47 2026-03-21 20:16:47,889 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-03-22 01:46:47 2026-03-21 20:16:47,890 INFO sqlalchemy.engine.Engine SELECT users.username, users.hashed_password, users.is_active, users.id, users.created_at, users.updated_at 
2026-03-22 01:46:47 FROM users 
2026-03-22 01:46:47 WHERE users.id = $1::UUID
2026-03-22 01:46:47 2026-03-21 20:16:47,890 INFO sqlalchemy.engine.Engine [cached since 3660s ago] (UUID('65f5b699-1b79-4510-8206-85c128fb87e1'),)
2026-03-22 01:46:47 2026-03-21 20:16:47,894 INFO sqlalchemy.engine.Engine SELECT scan_jobs.status, scan_jobs.job_type, scan_jobs.total, scan_jobs.processed, scan_jobs.error, scan_jobs.started_at, scan_jobs.completed_at, scan_jobs.created_at, scan_jobs.id 
2026-03-22 01:46:47 FROM scan_jobs 
2026-03-22 01:46:47 WHERE scan_jobs.id = $1::UUID
2026-03-22 01:46:47 2026-03-21 20:16:47,894 INFO sqlalchemy.engine.Engine [cached since 1747s ago] (UUID('d38b864e-3938-40ef-8c27-7b2df093cbed'),)
2026-03-22 01:46:47 2026-03-21T20:16:47.901490Z [info     ] request_completed              duration_ms=30.11 method=GET path=/api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed request_id=e71642e1 status_code=200
2026-03-22 01:46:47 INFO:     192.168.65.1:47298 - "GET /api/v1/migrate/jobs/d38b864e-3938-40ef-8c27-7b2df093cbed HTTP/1.1" 200 OK
2026-03-22 01:46:47 2026-03-21 20:16:47,904 INFO sqlalchemy.engine.Engine COMMIT
CELERY Logs - Job: 2.
"""
[2026-03-22 01:49:44,195: INFO/MainProcess] Task fortiq.classify_endpoints[17694fc9-e975-4a24-8a28-4455780eb474] received
[2026-03-22 01:49:44,218: INFO/MainProcess] Task fortiq.run_migration[0a5f4e84-c1a4-4b44-8f3b-d90902f1a9d2] received
objc[38476]: +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called.
objc[38476]: +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called. We cannot safely call it or ignore it in the fork() child process. Crashing instead. Set a breakpoint on objc_initializeAfterForkError to debug.
objc[38478]: +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called.
objc[38478]: +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called. We cannot safely call it or ignore it in the fork() child process. Crashing instead. Set a breakpoint on objc_initializeAfterForkError to debug.
objc[38479]: +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called.
objc[38479]: +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called. We cannot safely call it or ignore it in the fork() child process. Crashing instead. Set a breakpoint on objc_initializeAfterForkError to debug.
[2026-03-22 01:49:44,600: ERROR/MainProcess] Process 'ForkPoolWorker-5' pid:38476 exited with 'signal 6 (SIGABRT)'
[2026-03-22 01:49:44,620: ERROR/MainProcess] Task handler raised error: WorkerLostError('Worker exited prematurely: signal 6 (SIGABRT) Job: 4.')
Traceback (most recent call last):
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/billiard/pool.py", line 1265, in mark_as_worker_lost
    raise WorkerLostError(
    ...<2 lines>...
    )
billiard.einfo.ExceptionWithTraceback: 
"""
Traceback (most recent call last):
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/billiard/pool.py", line 1265, in mark_as_worker_lost
    raise WorkerLostError(
    ...<2 lines>...
    )
billiard.exceptions.WorkerLostError: Worker exited prematurely: signal 6 (SIGABRT) Job: 4.
"""
[2026-03-22 01:49:45,133: ERROR/MainProcess] Process 'ForkPoolWorker-6' pid:38478 exited with 'signal 6 (SIGABRT)'
[2026-03-22 01:49:45,157: ERROR/MainProcess] Task handler raised error: WorkerLostError('Worker exited prematurely: signal 6 (SIGABRT) Job: 5.')
Traceback (most recent call last):
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/billiard/pool.py", line 1265, in mark_as_worker_lost
    raise WorkerLostError(
    ...<2 lines>...
    )
billiard.einfo.ExceptionWithTraceback: 
"""
Traceback (most recent call last):
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/billiard/pool.py", line 1265, in mark_as_worker_lost
    raise WorkerLostError(
    ...<2 lines>...
    )
billiard.exceptions.WorkerLostError: Worker exited prematurely: signal 6 (SIGABRT) Job: 5.
"""
[2026-03-22 01:49:45,524: ERROR/MainProcess] Process 'ForkPoolWorker-7' pid:38479 exited with 'signal 6 (SIGABRT)'
[2026-03-22 01:49:45,543: ERROR/MainProcess] Task handler raised error: WorkerLostError('Worker exited prematurely: signal 6 (SIGABRT) Job: 6.')
Traceback (most recent call last):
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/billiard/pool.py", line 1265, in mark_as_worker_lost
    raise WorkerLostError(
    ...<2 lines>...
    )
billiard.einfo.ExceptionWithTraceback: 
"""
Traceback (most recent call last):
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/billiard/pool.py", line 1265, in mark_as_worker_lost
    raise WorkerLostError(
    ...<2 lines>...
    )
billiard.exceptions.WorkerLostError: Worker exited prematurely: signal 6 (SIGABRT) Job: 6.
"""
[2026-03-22 01:50:40,180: INFO/MainProcess] Task fortiq.run_migration[c3d8e8cc-c59d-433c-a2cd-f43f8c2eee7d] received
objc[38490]: +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called.
objc[38490]: +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called. We cannot safely call it or ignore it in the fork() child process. Crashing instead. Set a breakpoint on objc_initializeAfterForkError to debug.
[2026-03-22 01:50:40,687: ERROR/MainProcess] Process 'ForkPoolWorker-10' pid:38490 exited with 'signal 6 (SIGABRT)'
[2026-03-22 01:50:40,725: ERROR/MainProcess] Task handler raised error: WorkerLostError('Worker exited prematurely: signal 6 (SIGABRT) Job: 7.')
Traceback (most recent call last):
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/billiard/pool.py", line 1265, in mark_as_worker_lost
    raise WorkerLostError(
    ...<2 lines>...
    )
billiard.einfo.ExceptionWithTraceback: 
"""
Traceback (most recent call last):
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/billiard/pool.py", line 1265, in mark_as_worker_lost
    raise WorkerLostError(
    ...<2 lines>...
    )
billiard.exceptions.WorkerLostError: Worker exited prematurely: signal 6 (SIGABRT) Job: 7.
"""


PQC ERROR - 
"GET /api/v1/classify/model-comparison HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/fastapi/applications.py", line 1160, in __call__
    await super().__call__(scope, receive, send)
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/applications.py", line 107, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/middleware/base.py", line 191, in __call__
    with recv_stream, send_stream, collapse_excgroups():
                                   ~~~~~~~~~~~~~~~~~~^^
  File "/Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/contextlib.py", line 162, in __exit__
    self.gen.throw(value)
    ~~~~~~~~~~~~~~^^^^^^^
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/_utils.py", line 87, in collapse_excgroups
    raise exc
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/middleware/base.py", line 193, in __call__
    response = await self.dispatch_func(request, call_next)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/r17/Code/Fortiq/backend/app/core/logging.py", line 67, in dispatch
    response = await call_next(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/middleware/base.py", line 168, in call_next
    raise app_exc from app_exc.__cause__ or app_exc.__context__
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/middleware/base.py", line 144, in coro
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/middleware/cors.py", line 95, in __call__
    await self.simple_response(scope, receive, send, request_headers=headers)
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/middleware/cors.py", line 153, in simple_response
    await self.app(scope, receive, send)
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/routing.py", line 716, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/routing.py", line 736, in app
    await route.handle(scope, receive, send)
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/routing.py", line 290, in handle
    await self.app(scope, receive, send)
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 130, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 116, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 670, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "/Users/r17/Code/Fortiq/backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 324, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/r17/Code/Fortiq/backend/app/routers/classify.py", line 73, in get_model_comparison
    result = await db.execute(select(ModelEvaluation).order_by(ModelEvaluation.created_at.desc()).limit(2))
                                                               ^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: type object 'ModelEvaluation' has no attribute 'created_at'
2026-03-22 01:51:38,169 INFO sqlalchemy.engine.Engine SELECT endpoints.name, endpoints.host, endpoints.port, endpoints.endpoint_type, endpoints.algorithm, endpoints.key_length, endpoints.data_sensitivity, endpoints.exposure_surface, endpoints.traffic_volume, endpoints.cert_expiry_days, endpoints.risk_tier, endpoints.risk_score, endpoints.migration_status, endpoints.migrated_algorithm, endpoints.last_scanned_at, endpoints.id, endpoints.created_at, endpoints.updated_at 
FROM endpoints ORDER BY endpoints.risk_score DESC NULLS LAST 
 LIMIT $1::INTEGER OFFSET $2::INTEGER
2026-03-22 01:51:38,169 INFO sqlalchemy.engine.Engine [cached since 101.2s ago] (100, 0)
2026-03-21T20:21:38.255809Z [info     ] request_completed              duration_ms=451.54 method=GET path=/api/v1/endpoints request_id=5a6e8813 status_code=200
INFO:     127.0.0.1:58866 - "GET /api/v1/endpoints?per_page=100 HTTP/1.1" 200 OK
2026-03-22 01:51:38,260 INFO sqlalchemy.engine.Engine COMMIT