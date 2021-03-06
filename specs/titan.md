# The titan:project

The titan:project /has a :src-dir that /stores files from the mnieber/test:git-repository.
:It /has a frontend:service that is /configured in the frontend:layer.
:It /has a backend:service that is /configured in the backend:layer.
:It /uses a :vscode-project.

## The config:layer and stack:layer

The titan:project /has a config:layer that /has a service:layer-group that /contains the stack:layer, frontend:layer and backend:layer.
:It /has a :docker-compose and a dev:docker-compose file that are used
to /run the frontend:service and backend:service.
Both :docker-compose and dev:docker-compose are /configured by the stack:layer.

## The frontend:service

### Docker

The frontend:service /has a :dockerfile and a dev:dockerfile that /use the node:14-alpine:docker-image.
:It /uses the default:root-dir and default:src-mount-point.
:It /uses the :fish shell.
:It /uses the 3000:port.

### The react application

The frontend:service /has a :node-package.
:It /uses :create-react-app, :tailwind-css, :prettier, js:vandelay and :antd.
:It /has an app:module, donations:module and a donors:module.
:It /uses a :mock-graphql-server.

#### The app:module (app:x)

The app:module /defines an app:frame that /has a top:panel.
:It /has a :router and an app:store.

#### The donations:module

The donations:module /has a donations:store that /stores the donation:item-list.
:It /has a graphql:api that /provides the donation:item-list.
:It /has a donation:form-view, cancel-donation:view and a thank-you:view.

#### The donors:module

The donors:module /has a donors:store that /stores the donor:item-list.
:It /has a graphql:api that /provides the donor:item-list.
:It /has a donor:list-view that /has a selection:behavior.
:It /has a donor:item-view and a welcome-donor:view.

## The backend:service

### Docker

The backend:service /has a :dockerfile and a dev:dockerfile that /use the python:3:docker-image.
:It /uses the 8000:port.
:It /uses the default:root-dir and default:src-mount-point.
:It /has an :opt-dir to synchronize auxiliary files with the host.
:It /uses the :fish shell.

### The Django application

The backend:service /runs :django.
:It /has a :setup.cfg file.
:It /has a :makefile for /running :pip-compile.
:It /uses (:pytest /with :pytest-html), :pudb and :isort.
