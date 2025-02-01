setlocal
call %~dp0setup_venv.bat

pushd ..

rd /s /q build
rd /s /q dist
rd /s /q utf_queue_client.egg-info

python setup.py sdist bdist_wheel

popd
