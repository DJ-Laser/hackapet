{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  setuptools-scm,
  wheel,
  adafruit-circuitpython-connectionmanager,
}:
buildPythonPackage rec {
  pname = "adafruit_circuitpython_requests";
  version = "4.1.9";

  propagatedBuildInputs = [adafruit-circuitpython-connectionmanager];

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-ue6yUrQ5RvGpDDTKiETge7HgHNIQySf1YdDhC5fF/50=";
  };

  pyproject = true;
  build-system = [
    setuptools-scm
    setuptools
    wheel
  ];

  dontCheckRuntimeDeps = true;
}
