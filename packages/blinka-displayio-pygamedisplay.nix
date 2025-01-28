{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  setuptools-scm,
  wheel,
  pygame,
  adafruit-blinka-displayio,
}:
buildPythonPackage rec {
  pname = "blinka-displayio-pygamedisplay";
  version = "2.4.0";

  propagatedBuildInputs = [pygame adafruit-blinka-displayio];

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-rr2q2qOKZD3XeUnnauRiY7lPZw7dY0TcRPobqodZkdY=";
  };

  pyproject = true;
  build-system = [
    setuptools-scm
    setuptools
    wheel
  ];
}
