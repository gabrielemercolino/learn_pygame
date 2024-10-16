{
  description = "Example game made with pygame to learn the library";
  
  outputs = { self, nixpkgs, flake-utils, pyproject-nix, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python312;
        
        game = pyproject-nix.lib.project.loadPyproject { projectRoot = ./game; };
        game-attrs = game.renderers.buildPythonPackage { inherit python; };
        
        editor = pyproject-nix.lib.project.loadPyproject { projectRoot = ./editor; };
        editor-attrs = editor.renderers.buildPythonPackage { inherit python; };
      in
      {
        packages.learn_pygame_game = python.pkgs.buildPythonPackage game-attrs; 
        packages.learn_pygame_editor = python.pkgs.buildPythonPackage editor-attrs;

        apps.default = {
          type = "app";
          program = "${self.packages.${system}.learn_pygame_game}/bin/game";
        };

        apps.editor = {
          type = "app";
          program = "${self.packages.${system}.learn_pygame_editor}/bin/editor";
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [ python python.pkgs.pygame-ce python.pkgs.attrs];
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

