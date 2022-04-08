{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/30d3d79b7d3607d56546dd2a6b49e156ba0ec634.tar.gz") {}}:

let
  my-python = pkgs.python39;
  python-with-my-packages = my-python.withPackages (p: with p; [
    pandas
    requests
    pytest
    # other python packages you want
  ]);
in
pkgs.mkShell {
  buildInputs = [
    python-with-my-packages
    pkgs.git
    pkgs.which
    # other dependencies
  ];
  shellHook = ''
    PYTHONPATH=${python-with-my-packages}/${python-with-my-packages.sitePackages}
  '';
}
