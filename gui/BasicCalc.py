import re
import tkinter as tk
from tkinter import StringVar, ttk

class BasicCalc:
	def __init__(self, root, frame):
		'''Intialize BasicCalc object with the inpur root widget and frame'''
		# Root frame, the main app window
		self.root = root
		# Frame for this widget, the tab for this widget
		self.frame = frame

		# Configure the grid format of the widget's frame, so
		# that each row and column is the same size
		self.frame.columnconfigure(tuple(range(4)), weight=1)
		self.frame.rowconfigure(tuple(range(6)), weight=1)
		# Event bindings if a keyboard key or Enter is pressed
		self.root.bind("<Key>", self.key_press)
		self.root.bind('<Return>', self.solve_eqn)

		# Holds the current equation, generally is the same as
		# self.equation, except when an invalid calculation is
		# tried.
		self.expression = ""
		# The equation that is displayed in the Entry window
		self.equation = StringVar()
		# Flag to indicate whether the total from a previous
		# equation is being displayed
		self.total_flag=False

		# Frame for holding the Entry widget, used for border styling and padding around the Entry
		frm_equation = tk.Frame(self.frame, borderwidth=5, relief=tk.SUNKEN, padx=10)
		frm_equation.grid(columnspan=4, sticky=tk.N+tk.S+tk.E+tk.W, padx=20)
		frm_equation.columnconfigure(0, weight=1)
		frm_equation.rowconfigure(0, weight=1)
		# Entry widget, is disabled so that no cursor is present,
		# and direct text entry is not enabled
		ent_equation = tk.Entry(frm_equation, textvariable=self.equation,
														borderwidth=0, relief=tk.FLAT, justify=tk.RIGHT,
														state="disabled", font="Calibri 20",
														disabledforeground="black")
		ent_equation.grid(columnspan=4, sticky=tk.N+tk.S+tk.E+tk.W)

		# Calculator buttons, with the text of the button as the dict key
		# and the [row, col] coordinates as the dict values
		but_coords = { "AC": [0,0], "+/-": [0,1], "%": [0,2], "/": [0,3],
									 7: [1,0], 8: [1,1], 9: [1,2], "*": [1,3],
									 4: [2,0], 5: [2,1], 6: [2,2], "-": [2,3],
									 1: [3,0], 2: [3,1], 3: [3,2], "+": [3,3],
									 0: [4,0], ".": [4,2], "=":[4,3] }
		# Create each button and place it on the grid
		for button in but_coords:
			new_but = tk.Button(self.frame, text=f' {button} ', fg='black', bg='green',
												command=lambda button=button: self.but_press(button),
											 	height=1, width=7)
			# The 0 button is double wide, similar to iOS calculator
			if button == 0:
				new_but.grid(row=(but_coords[button][0]+1), column=but_coords[button][1], columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
			else:
				new_but.grid(row=(but_coords[button][0]+1), column=but_coords[button][1], sticky=tk.N+tk.S+tk.E+tk.W)


	def but_press(self, button):
		'''Carry out the correct action when a calculator button is clicked'''
		# Solve the input expression
		if button == "=":
			self.solve_eqn(None)
		# Clear the input expression
		elif button == "AC":
			self.expression = ""
			self.equation.set("")
		# Negate the current number
		elif button == "+/-":
			self.negate_num()
		# Add the button's value to the expression string
		else:
			self.update_eqn(button)


	def key_press(self, event):
		'''Carry out the correct action when a keyboard key is pressed'''
		key = str(event.char)
		# If the key is a number, decimal, or operator, add it to the
		# input expression
		if key.isdigit() or key in "+-*/%.":
			self.update_eqn(key)
		# If the key is the equals key, solve the input expression
		elif key == "=":
			self.solve_eqn()
		# If the key is something else, ignore it


	def change_operation(self, operation):
		'''Change the operator at the end of the expression to the input operation'''
		# If the last two chars are "-", then the first is a minus
		# sign and should be changed
		if self.expression[-1:] == "-" and self.expression[-2:-1] in "+-*/%":
			self.expression = self.expression[0:-2] + str(operation) + self.expression[-1:]
			self.equation.set(self.expression)
		# Otherwise just the last char should be changed
		else:
			self.expression = self.expression[0:-1] + str(operation)
			self.equation.set(self.expression)


	def negate_num(self):
		'''Add or remove a negative sign based on what the current expression is'''
		# Indices for getting chars from the input expression
		i=-1
		j=0
		# The end char in the expression
		curr_char = self.expression[i:]
		# If its an operator (that isn't a minus sign), just add a negative sign
		if curr_char in "+*/%":
			self.expression = self.expression + "-"
			self.equation.set(self.expression)
		else:
			# Get the next char, which is the char before the current char
			i-=1
			j-=1
			next_char = self.expression[i:j]
			# If the end char is a number, including the decimal point in a number
			if curr_char.isdigit() or curr_char == ".":
				# Iterate backwards through the expression until the
				# next char is not a digit.
				while next_char.isdigit() or next_char == ".":
					i-=1
					j-=1
					curr_char = next_char
					next_char = self.expression[i:j]

			# If both current char and next char are either a minus
			# or not a minus (logical XNOR)
			if not (curr_char == "-") ^ (next_char == "-"):
				self.expression = self.expression[:j] + "-" + self.expression[j:]
			# Else if only current char is a minus
			elif curr_char == "-":
				self.expression = self.expression[:j]
			# Else if only next char is minus
			else:
				self.expression = self.expression[:i] + self.expression[j:]

			# Update the equation based on the expression
			self.equation.set(self.expression)


	def update_eqn(self, char):
		'''Add a character to the expression, and update the equation'''
		# If the current expression is the result from the previous expression,
		# and a number or decimal point is input, clear the expression first
		if self.total_flag and (str(char).isdigit() or str(char) == "."):
			self.expression = ""
		# Indicates the current expression is no long the result of the previous
		# expression, as it was either just reset, or something is being added to it
		self.total_flag=False

		# If an operator was selected
		if str(char) in "+-*/%":
			# If the expression is empty and the input char isn't a negative sign, or the
			# expression only contains a decimal point or a negative sign, set the expression
			# to contain only a zero, so that the operator can be added after that
			if (self.expression == "" and str(char) != "-") or self.expression == "." or self.expression == "-":
				self.expression = "0"
			# If the last char in the expression is already an operator, change it to the new one
			if self.expression[-1:] in "+-*/%":
				self.change_operation(char)
			# Otherwise just append the operator
			else:
				self.expression = self.expression + str(char)
				self.equation.set(self.expression)
		elif str(char) == ".":
			# If the expression is empty or the end char is an operator,
			# append a zero before appending the decimal
			if self.expression == "" or self.expression[-1:] in "+-*/%":
				self.expression = self.expression + "0" + str(char)
				self.equation.set(self.expression)
			else:
				# Split the expression at each operator
				exp_list = re.split('\+|\-|\*|/|%', self.expression)
				# If the end number doesn't contain a decimal, append it,
				# otherwise ignore the new decimal input
				if "." not in exp_list[-1]:
					self.expression = self.expression + str(char)
					self.equation.set(self.expression)
		else:
			self.expression = self.expression + str(char)
			self.equation.set(self.expression)

	def solve_eqn(self, event):
		'''Try and solve the current equation'''
		# If there isn't any expression, don't change anything
		if self.expression == "":
			return
		try:
			# Format the total to be a max of 15 digits, and remove any
			# trailing zeros and decimals
			total = str(('%.15f' % eval(self.expression)).rstrip('0').rstrip('.'))
			self.equation.set(total)
			self.expression = total
			self.total_flag=True
		except:
			self.equation.set(" NaN ")
			self.expression = ""

