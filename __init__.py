from aqt import mw
from aqt.reviewer import Reviewer
from PyQt6.QtCore import QTimer

original_show_answer = Reviewer._showAnswer

def custom_show_answer(self, *args, **kwargs):
    result = original_show_answer(self, *args, **kwargs)

    def highlight_button():

        rows = mw.col.db.execute(
            "SELECT ease FROM revlog WHERE cid = ? ORDER BY id DESC LIMIT 1",
            self.card.id
        )

        if not rows:
            return

        last_ease = rows[0][0]

        js = f"""
        function highlight() {{
            let btn = document.querySelector('button[data-ease="{last_ease}"]');

            if (btn) {{
                btn.style.setProperty("background-color", "#FFB347", "important");
                btn.style.setProperty("border", "2px solid white", "important");
            }}
        }}

        // run multiple times because Anki re-renders DOM
        highlight();
        setTimeout(highlight, 200);
        setTimeout(highlight, 500);
        setTimeout(highlight, 1000);
        """

        self.bottom.web.page().runJavaScript(js)

    QTimer.singleShot(300, highlight_button)

    return result

Reviewer._showAnswer = custom_show_answer