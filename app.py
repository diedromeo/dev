from flask import Flask, render_template_string, session, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Flag for CTF
FLAG = "ctf7{You_are_the_Ultimate_Dev}"

# Base HTML template with orange, black, white, and green color scheme
BASE_HTML = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Flask CTF Challenge</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #121212;
            color: #ffffff;
            padding: 50px;
            text-align: center;
        }
        h1 {
            color: #ff6600; /* Orange */
            font-size: 48px;
        }
        .btn {
            padding: 20px 40px;
            background-color: #00ff88; /* Green */
            border: none;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            cursor: pointer;
        }
        .btn:disabled {
            background-color: #555; /* Grey when disabled */
            cursor: not-allowed;
        }
        .mock {
            color: #ff6347; /* Red */
            font-size: 24px;
            margin-top: 30px;
        }
        .footer {
            margin-top: 50px;
            color: #d6d6d6; /* Light Grey */
        }
        .gif-container {
            display: none;
            margin-top: 30px;
            text-align: center;
        }
        .gif-container img {
            width: 300px;
        }
    </style>
</head>
<body>
    <h1>Welcome, Future Developer! 💻</h1>
    <p>Are you ready to prove your skills and unlock the ultimate developer status? 🚀</p>
    
    <!-- Button that will be disabled initially -->
    <button class="btn" id="flagButton" disabled>Get Flag 🏆</button>

    <p class="mock">Your mission, should you choose to accept it. 👨‍💻 Can you do it? 💥</p>

    <div class="gif-container">
        <p><strong>Nice try! You're getting closer... 🔥</strong></p>
        <img src="https://i.giphy.com/qgcr4xCumRRqLyN6ia.webp" alt="GIF" />
    </div>

    <footer class="footer">
        <p>CTF Challenge - Brought to you by the *Ultimate Developer's Academy* 😎</p>
    </footer>

    <script>
        let rightClickCount = 0; // Variable to count right-clicks

        // Show the GIF when the user right-clicks
        document.addEventListener("contextmenu", function(e) {
            e.preventDefault();  // Disable right-click menu

            rightClickCount++;

            if (rightClickCount === 1) {
                // Show the GIF for the first right-click
                document.querySelector(".gif-container").style.display = "block";
            } else if (rightClickCount === 2) {
                // Encourage the user to inspect the page after the second right-click
                alert("🔧 Let's see if you can unlock your developer skills!");
            }
        });

        // If the user clicks the enabled button, send them to the flag (AJAX call)
        document.getElementById("flagButton").addEventListener("click", function() {
            fetch('/enable_flag', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.flag) {
                    alert("🚀 You've become the Ultimate Developer! 👩‍💻");
                    window.location.href = '/get_flag'; // Redirect to the flag route
                } else {
                    alert("🚫 Something went wrong. Please try again!");
                }
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(BASE_HTML)

@app.route('/get_flag')
def get_flag():
    # Serve the flag only if the button has been enabled
    if 'enabled' in session and session['enabled']:
        return f"<h2>Flag: {FLAG}</h2>"
    else:
        # If the user tries to access the flag without enabling the button
        return "<h2>Error: You need to enable the button first!</h2>"

@app.route('/enable_flag')
def enable_flag():
    # This route is called via AJAX, only enabling flag access if button is unlocked
    if 'enabled' in session and session['enabled']:
        return jsonify({'flag': True})
    else:
        return jsonify({'flag': False})

@app.route('/enable_button')
def enable_button():
    # Set session flag when button is enabled
    session['enabled'] = True
    return redirect(url_for('home'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
