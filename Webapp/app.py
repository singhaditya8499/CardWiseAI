from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', output_text='')

@app.route('/', methods=['POST'])
def process_input():
    user_input = request.form['user_input']
    # Call your function here to process user input and generate text
    processed_text = process_user_input(user_input)
    return render_template('index.html', output_text=processed_text)

def process_user_input(input_text):
    # Replace this function with your own logic to process the input
    # For this example, we'll just return the input text as is
    return input_text

if __name__ == '__main__':
    app.run(debug=True)
