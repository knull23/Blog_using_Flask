from flask import Flask, render_template, request
import requests
import smtplib

# Fetching posts from the API
posts = requests.get("https://api.npoint.io/b836130122635f1d6adc").json()

# Email credentials
MY_EMAIL = "saumil.upadhyay@gmail.com"
MY_PASSWORD = "mjixlfkuddsfiljg"

app = Flask(__name__)


# Route to get all posts
@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


# Route to show a specific post based on its index
@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for post in posts:
        if post["id"] == index:
            requested_post = post
    return render_template("post.html", post=requested_post)


# Route to show about page
@app.route("/about")
def about():
    return render_template("about.html")


# Route to handle contact form submissions
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


# Function to send email
def send_email(name, email, phone, message):
    email_message = f"Subject: New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:  # Use port 587 for TLS
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=email_message.encode('utf-8')  # Ensure message is UTF-8 encoded
        )


if __name__ == "__main__":
    app.run(debug=True, port=5001)

