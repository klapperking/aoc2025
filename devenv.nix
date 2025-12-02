{
  pkgs,
  inputs,
  ...
}:
let
  pkgs-unstable = import inputs.nixpkgs-unstable { system = pkgs.stdenv.system; };
in
{
  cachix.enable = false;
  difftastic.enable = true;

  packages = [
    pkgs-unstable.git
    pkgs-unstable.just
  ];

  languages.python = {
    enable = true;
    package = pkgs-unstable.python313;
    uv = {
      enable = true;
    };
  };
}
