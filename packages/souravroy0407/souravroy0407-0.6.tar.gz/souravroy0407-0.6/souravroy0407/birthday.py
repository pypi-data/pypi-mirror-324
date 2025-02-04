import webbrowser
import os

def dora():
    # HTML message content
    message = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Happy Birthday Dora</title>
        <style>
            body {
                background-color: #f4f4f9;
                font-family: 'Arial', sans-serif;
                color: #333;
                line-height: 1.6;
                padding: 20px;
                text-align: center;
            }

            h1 {
                font-size: 2.5em;
                color: #D35400;
                margin-bottom: 20px;
            }

            .message-container {
                width: 80%;
                max-width: 800px;
                margin: 0 auto;
                text-align: left;  /* Keep text left-aligned inside the container */
                background-color: #fff;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }

            .highlight {
                font-weight: bold;
                color: #E74C3C;
            }

            .emoji {
                font-size: 2em;
            }

            .birthday-message {
                font-size: 1.2em;
                color: #2C3E50;
                margin: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Happy Birthday Dora MadamJi! 🎉</h1>
        <div class="message-container">
            <p class="birthday-message">
                Dear Dora MadamJi <span class="emoji">😘❤</span>,<br><br>
                On this special day, I just want to remind you how much you mean to me.<br><br>
                First of all, happy birthday! Many, many happy returns of the day 🌹😀.<br><br>
                Thank you for coming into my life. Before you came, and after you came, there is a huge difference between these two things.<br><br>
                I've never received love like this from anyone before.<br><br>
                You wanted to know what made me like you? So listen, the main thing that attracts me about you is your mindset (self-dependent, open-minded, focused, etc.)—nothing else. When I observed you, I realized yes, I was looking for someone like that. I wanted someone to guide me in my life, and that’s what I saw in you.<br><br>
                And for that, I love you so much and will always love you so much. I love you, Dora 💖 😘.<br><br>
                Onek English hoye gache, ebar ektu Bangla-te boli 😶. Ha, aro ekta important thing, ektu kom taka nosto koro. Amer opar koto kosto kore to income koros tar opar nijer opar o spend kora bondho kora deyachis, sob khali buber jonne dile ki kore hobe...<br><br>
                2 mas hoye gelo amader relationship e. Still, ame Bindu tuku kono change dekte parchi. Sei first din-er moto, tan sei bhalo basa, sei rokom vabe care kore jachis.<br><br>
                Tui bolis na, tor sathe khotau gurte berole tui naki tor brain off kore dis, r sob amar opar chara dis. R amar dik ta dekhe ame to vabai chara deyachi tui aser por deya eta korbo kina, ota korle thike hobe kina.<br><br>
                Ses e etai bolbi, sotti ekta mon er moto life partner payechi r harate chai na. Always stay with me please 🥺.<br><br>
                I love you more and more 💗.<br><br>
                Happy birthday Dora ❤.<br><br>
            </p>
        </div>
    </body>
    </html>
    """

    
    # File name
    file_name = "birthday_message_dora.html"
    
    # Write the message to an HTML file
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(message)
    
    # Open the file in the default web browser
    file_path = os.path.abspath(file_name)
    webbrowser.open(f'file://{file_path}')
