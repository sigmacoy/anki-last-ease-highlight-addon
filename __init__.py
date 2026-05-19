from aqt import mw
from aqt.reviewer import Reviewer

original_show_answer = Reviewer._showAnswer

def custom_show_answer(self, *args, **kwargs):
    result = original_show_answer(self, *args, **kwargs)
    
    # Get most recent ease from revlog for this card
    cursor = mw.col.db.execute(
        "SELECT ease FROM revlog WHERE cid = ? ORDER BY id DESC LIMIT 1",
        self.card.id
    )
    row = cursor.fetchone()
    
    if row and row[0] in [1, 2, 3, 4]:
        last_ease = row[0]
        buttons = self.bottom.web.findElements("button")
        
        # Ease values: 1=Again, 2=Hard, 3=Good, 4=Easy
        if buttons and last_ease - 1 < len(buttons):
            buttons[last_ease - 1].setAttribute(
                "style", 
                "background-color: #FFB347 !important;"
            )
    
    return result

Reviewer._showAnswer = custom_show_answer