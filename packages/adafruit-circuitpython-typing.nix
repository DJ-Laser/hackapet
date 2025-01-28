{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  setuptools-scm,
  wheel,
  adafruit-blinka,
  adafruit-circuitpython-busdevice,
  adafruit-circuitpython-requests,
}:
buildPythonPackage rec {
  pname = "adafruit_circuitpython_typing";
  version = "1.11.2";

  propagatedBuildInputs = [adafruit-circuitpython-busdevice adafruit-circuitpython-requests];

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-x6yFMqmtfkpl1ViHZLdIPAtpZ9MFw3+uvMDFNW1nfjM=";
  };

  pyproject = true;
  build-system = [
    setuptools-scm
    setuptools
    wheel
  ];

  dontCheckRuntimeDeps = true;
}
