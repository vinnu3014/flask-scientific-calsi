from flask import Flask, render_template, request, jsonify
import math
import json

app = Flask(__name__)

class ScientificCalculator:
    def __init__(self):
        self.memory = 0
    
    def calculate(self, expression):
        try:
            # Replace mathematical function names with Python equivalents
            expression = expression.replace('π', 'pi')
            
            # Safely evaluate the expression
            result = eval(expression, {"__builtins__": {}}, {
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "sqrt": math.sqrt,
                "log": math.log10,
                "ln": math.log,
                "asin": math.asin,
                "acos": math.acos,
                "atan": math.atan,
                "pi": math.pi,
                "e": math.e,
                "factorial": math.factorial,
                "radians": math.radians,
                "degrees": math.degrees,
                "abs": abs,
                "pow": pow,
            })
            return round(result, 10)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def memory_add(self, value):
        try:
            self.memory += float(value)
            return self.memory
        except Exception:
            return self.memory
    
    def memory_subtract(self, value):
        try:
            self.memory -= float(value)
            return self.memory
        except Exception:
            return self.memory
    
    def memory_clear(self):
        self.memory = 0
        return self.memory
    
    def memory_recall(self):
        return self.memory

calculator = ScientificCalculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        expression = data.get('expression', '')
        
        if not expression:
            return jsonify({'result': 0})
        
        result = calculator.calculate(expression)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'result': f'Error: {str(e)}'})

@app.route('/memory-add', methods=['POST'])
def memory_add():
    data = request.json
    value = data.get('value', 0)
    result = calculator.memory_add(value)
    return jsonify({'memory': result})

@app.route('/memory-subtract', methods=['POST'])
def memory_subtract():
    data = request.json
    value = data.get('value', 0)
    result = calculator.memory_subtract(value)
    return jsonify({'memory': result})

@app.route('/memory-recall', methods=['GET'])
def memory_recall():
    result = calculator.memory_recall()
    return jsonify({'memory': result})

@app.route('/memory-clear', methods=['POST'])
def memory_clear():
    result = calculator.memory_clear()
    return jsonify({'memory': result})

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, host='127.0.0.1', port=8080)
