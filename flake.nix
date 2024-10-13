{
  description = "template dev flake";
  
  outputs = { self, nixpkgs, flake-utils, pyproject-nix, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python312;
        project = pyproject-nix.lib.project.loadPyproject {
          projectRoot = ./.;
        };
        attrs = project.renderers.buildPythonPackage { inherit python; };
      in
      {
        packages.learn_pygame = python.pkgs.buildPythonPackage attrs; 

        apps.default = {
          type = "app";
          program = "${self.packages.${system}.learn_pygame}/bin/learn_pygame";
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [ python python.pkgs.pygame-ce ];  # Aggiungi Python e Pygame alla shell
        };
      }
    );

  inputs = {
    nixpkgs.url     = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
}

