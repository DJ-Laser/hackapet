{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  setuptools-scm,
  wheel,
  adafruit-blinka,
}:
buildPythonPackage rec {
  pname = "adafruit_circuitpython_connectionmanager";
  version = "3.1.3";

  propagatedBuildInputs = [];

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-DxM73t9FTt4MCoZu1gX+FmzIX3XPzqdHWONiKuQD5fk=";
  };

  pyproject = true;
  build-system = [
    setuptools-scm
    setuptools
    wheel
  ];

  dontCheckRuntimeDeps = true;
}
