from titan.react_pkg.pkg.builder import Builder


class KeyHandlerBuilder(Builder):
    type = "KeyHandler"

    def build(self):
        self.output.add(
            preamble=[tpl_preamble],
            lines=[tpl],
            imports=[
                "import * as R from 'ramda';",
                "import KeyboardEventHandler from 'react-keyboard-event-handler';",
                "import { createKeyDownHandler } from '/src/utils';",
            ],
        )
        self.output.set_flags(["app/keyboardHandler"])


tpl_preamble = """
    const keyHandlers = {
      'ctrl+shift+space': () => { console.log("Moonleap Todo"); },
    };

    const handledKeys = R.keys(keyHandlers);
    const onKeyDown = createKeyDownHandler(keyHandlers);
"""


tpl = """
    <KeyboardEventHandler handleKeys={handledKeys} onKeyEvent={onKeyDown}>
    {props.children}
    </KeyboardEventHandler>
"""
