{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  setuptools-scm,
  wheel,
  adafruit-platformdetect,
  adafruit-pureio,
  binho-host-adapter,
  pyftdi,
  adafruit-circuitpython-typing,
  sysv-ipc,
}:
buildPythonPackage rec {
  pname = "adafruit_blinka";
  version = "8.51.0";

  propagatedBuildInputs = [adafruit-platformdetect adafruit-pureio binho-host-adapter pyftdi adafruit-circuitpython-typing sysv-ipc];

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-hE8Vvnde5cQYRGlppCfFo4R5KOZE8rGjVUKs/1sgjzo=";
  };

  pyproject = true;
  build-system = [
    setuptools-scm
    setuptools
    wheel
  ];

  dontCheckRuntimeDeps = true;
}
