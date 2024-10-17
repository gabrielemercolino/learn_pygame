{
  description = "Example game made with pygame to learn the library";
  
  outputs = { nixpkgs, flake-utils, pyproject-nix, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python312;
        
        project = pyproject-nix.lib.project.loadPyprojectDynamic { projectRoot = ./.;};
        attrs = project.renderers.buildPythonPackage { inherit python; };
        learn_pygame = python.pkgs.buildPythonPackage attrs;
      in
      {
        packages.default = learn_pygame;

        apps.default = {
          type = "app";
          program = "${learn_pygame}/bin/game";
        };

        apps.editor = {
          type = "app";
          program = "${learn_pygame}/bin/editor";
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [ 
            python 
            (pkgs.poetry.override { python3 = python; })
            python.pkgs.pygame
            python.pkgs.attrs
            python.pkgs.numpy
          ];
        };
      }
    );

  inputs = {
    nixpkgs.url     = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url  = "github:nix-community/poetry2nix";
    pyproject-nix.url = "github:nix-community/pyproject.nix";
    pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";
  };
}

