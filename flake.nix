{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs @ {
    self,
    nixpkgs,
    flake-parts,
    poetry2nix,
    ...
  }:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = ["x86_64-linux"];

      perSystem = {pkgs, ...}: let
        inherit (poetry2nix.lib.mkPoetry2Nix {inherit pkgs;}) mkPoetryEnv defaultPoetryOverrides;
      in {
        formatter = pkgs.alejandra;
        devShells.default = pkgs.mkShell {
          shellHook = ''
            export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
              pkgs.stdenv.cc.cc
            ]}
          '';

          packages = with pkgs; [
            bash
            git
            coreutils
            moreutils
            diffutils
            black
            isort
            poetry
            stdenv.cc.cc.lib
          ];
        };
      };
    };
}
