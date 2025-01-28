{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";

    pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
    pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    pyproject-nix,
  } @ inputs:
    flake-utils.lib.eachDefaultSystem
    (
      system: let
        pkgs = import nixpkgs {inherit system;};
        lib = pkgs.lib;

        pyproject = pyproject-nix.lib.project.loadPyproject {projectRoot = ./.;};

        callAdafruitPackages = names: pypkgs: let
          packagesList =
            lib.map (name: {
              ${name} = pypkgs.callPackage ./packages/${name}.nix {};
            })
            names;
          packages = lib.foldl (a: b: a // b) {} packagesList;
        in
          packages
          // {
            adafruit = packages;
          };

        python = pkgs.python3.override {
          packageOverrides = pyfinal: pyprev:
            {
              mk-adafruit-lib = pyfinal.callPackage ./packages/mk-adafruit-lib.nix {};
            }
            // callAdafruitPackages [
              "blinka-displayio-pygamedisplay"
              "adafruit-blinka-displayio"
              "adafruit-blinka"
              "adafruit-circuitpython-typing"
              "adafruit-circuitpython-requests"
              "adafruit-circuitpython-busdevice"
              "adafruit-circuitpython-connectionmanager"
              "adafruit-circuitpython-bitmap-font"
              "adafruit-circuitpython-display-text"
            ]
            pyfinal;
        };

        projectPackages = pyproject.renderers.withPackages {inherit python;};

        pythonEnv = python.withPackages projectPackages;
      in {
        devShells.default = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [alejandra pythonEnv];
        };
      }
    );
}
