from leapreact.nodepackage import NodePackageConfig


def get():
    return NodePackageConfig(
        body={
            "dependencies": {
                "@craco/craco": "^6.0.0",
                "node-sass": "^4.0.0",
                "postcss": "^7",
                "tailwindcss": "npm:@tailwindcss/postcss7-compat",
            },
            "scripts": {
                "start": "craco start",
                "build": "craco build",
                "test": "craco test",
                "eject": "craco eject",
            },
        }
    )
