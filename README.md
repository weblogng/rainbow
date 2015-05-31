# Overview #
Rainbow supports [blue-green deployment](http://martinfowler.com/bliki/BlueGreenDeployment.html) of static web applications 
to nginx and emphasizes simplicity of operation and implementation.

Rainbow expects

* fabric to be pre-installed in the deployment toolchain
* used as an api from within your deployment-related fabfiles
* artifacts packaged as a tar.gz, which will be extracted on the target node filesystem
* nginx to serve the artifacts

# Usage #

Rainbow is expected to be used as an api from within the fabfile(s) used for application deployment.

Since Rainbow is an api, the resulting fabfile integration can look however you want, but Rainbow is designed to support a fab commands like:

Deploy the next release to production:

`fab deploy-next prod static-webapp-2015-04-18_20-24-25_UTC.35ccbf3.tar.gz`

Roll-forward (cut-over) to the 'next' release:

`fab roll-forward prod`

Roll-back (cut-over) to the 'previous' release:

`fab roll-back prod`

# Credits #

Rainbow was heavily-inspired by:

* [gitric](https://github.com/dbravender/gitric)
