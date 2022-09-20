import pytest
import tkinter as tk
from gui.BasicCalc import BasicCalc


class TestButPress:
  '''
  Test the BasicCalc.but_press function. Since this
  function primarily only calls other BasicCalc functions,
  which are tested elsewhere, complex test cases are not
  required for this function.

  Excluded Test Cases:
    None
  '''
  @pytest.fixture(autouse=True)
  def bc_fixture(self):
    '''A simulated BasicCalc object'''
    self.bc_fixture = BasicCalc(tk.Tk(), tk.Frame())

  def test_but_press_equals(self):
    '''Simulate the user hitting the "=" button'''
    self.bc_fixture.expression = "1+1"
    self.bc_fixture.but_press("=")
    assert self.bc_fixture.expression == "2"

  def test_but_press_AC(self):
    '''Simulate the user hitting the "AC" button'''
    self.bc_fixture.expression = "1+1"
    self.bc_fixture.but_press("AC")
    assert self.bc_fixture.expression == ""

  def test_but_press_negative(self):
    '''Simulate the user hitting the "+/-" button'''
    self.bc_fixture.expression = "1+1"
    self.bc_fixture.but_press("+/-")
    assert self.bc_fixture.expression == "1+-1"

  def test_but_press_number(self):
    '''Simulate the user hitting a number button'''
    self.bc_fixture.expression = "1+"
    self.bc_fixture.but_press(3)
    assert self.bc_fixture.expression == "1+3"

  def test_but_press_operator(self):
    '''Simulate the user hitting an operator button'''
    self.bc_fixture.expression = "1"
    self.bc_fixture.but_press("/")
    assert self.bc_fixture.expression == "1/"


class TestKeyPress:
  '''
  Test the BasicCalc.key_press function

  Excluded Test Cases:
    1) All test cases are excluded
        - The key_press function is based on a user event
          of pressing a keyboard key, which is difficult to
          simulate with pytest, and not worth the effort at
          this time
        - The key_press function essentially only calls the
          update_eqn function or solve_eqn function, so there
          is only a very minute loss of code coverage
  '''
  @pytest.fixture(autouse=True)
  def bc_fixture(self):
    '''A simulated BasicCalc object'''
    self.bc_fixture = BasicCalc(tk.Tk(), tk.Frame())

  @pytest.mark.skip(reason="See test class docstring for details.")
  def test_key_press(self):
    pass


class TestChangeOperation:
  '''
  Test the BasicCalc.change_operation function. Extra tests are
  included to ensure the correct changes are made when dealing
  with minus signs and negatives, as the "-" char can cause
  issues due to possibly being either a minus sign or a negative
  sign.

  Excluded Test Cases:
    1) Expression ending in a number or a decimal point
        - the change_operation function is only called if the
          expression ends with an operator
    2) Non-operator character being passed as the replacement
        - the change_operation function is only called when
          the button or key pressed is an operator
  '''
  @pytest.fixture(autouse=True)
  def bc_fixture(self):
    '''A simulated BasicCalc object'''
    self.bc_fixture = BasicCalc(tk.Tk(), tk.Frame())

  def test_change_same_op_no_minus_no_neg(self):
    '''Change operation to the same operation'''
    self.bc_fixture.expression = "3+"
    self.bc_fixture.change_operation("+")
    assert self.bc_fixture.expression == "3+"

  def test_change_diff_op_no_minus_no_neg(self):
    '''Change operation to a different operation, with neither operation being a minus'''
    self.bc_fixture.expression = "3+"
    self.bc_fixture.change_operation("*")
    assert self.bc_fixture.expression == "3*"

  def test_change_same_op_minus_no_neg(self):
    '''Change operation when both are minus'''
    self.bc_fixture.expression = "3-"
    self.bc_fixture.change_operation("-")
    assert self.bc_fixture.expression == "3-"

  def test_change_diff_op_minus_no_neg_1(self):
    '''Change operation to a minus'''
    self.bc_fixture.expression = "3+"
    self.bc_fixture.change_operation("-")
    assert self.bc_fixture.expression == "3-"

  def test_change_diff_op_minus_no_neg_2(self):
    '''Change operation from a minus'''
    self.bc_fixture.expression = "3-"
    self.bc_fixture.change_operation("+")
    assert self.bc_fixture.expression == "3+"

  def test_change_same_op_no_minus_neg(self):
    '''Change operation to the same operation when there is a negative present'''
    self.bc_fixture.expression = "3+-"
    self.bc_fixture.change_operation("+")
    assert self.bc_fixture.expression == "3+-"

  def test_change_diff_op_no_minus_neg(self):
    '''Change operation to a different operation when there is a negative present'''
    self.bc_fixture.expression = "3+-"
    self.bc_fixture.change_operation("*")
    assert self.bc_fixture.expression == "3*-"

  def test_change_same_op_minus_neg(self):
    '''Change operation when both are minus and there is a negative present'''
    self.bc_fixture.expression = "3--"
    self.bc_fixture.change_operation("-")
    assert self.bc_fixture.expression == "3--"

  def test_change_diff_op_minus_neg_1(self):
    '''Change operation to a minus when there is a negative present'''
    self.bc_fixture.expression = "3+-"
    self.bc_fixture.change_operation("-")
    assert self.bc_fixture.expression == "3--"
    
  def test_change_diff_op_minus_neg_1(self):
    '''Change operation from a minus when there is a negative present'''
    self.bc_fixture.expression = "3--"
    self.bc_fixture.change_operation("*")
    assert self.bc_fixture.expression == "3*-"


class TestNegateNum:
  '''
  Test the BasicCalc.negate_num function.

  Excluded Test Cases:
    None
  '''
  @pytest.fixture(autouse=True)
  def bc_fixture(self):
    '''A simulated BasicCalc object'''
    self.bc_fixture = BasicCalc(tk.Tk(), tk.Frame())

  def test_negate_num_no_num_no_neg_1(self):
    '''Negate the number before the number is entered (at the start of the expression) and without a negative present'''
    self.bc_fixture.expression = ""
    self.bc_fixture.negate_num()
    assert self.bc_fixture.expression == "-"

  def test_negate_num_no_num_no_neg_2(self):
    '''Negate the number before the number is entered (at the end of the expression) and without a negative present'''
    self.bc_fixture.expression = "3+"
    self.bc_fixture.negate_num()
    assert self.bc_fixture.expression == "3+-"

  def test_negate_num_num_no_neg(self):
    '''Negate the number after the number is entered and without a negative present'''
    self.bc_fixture.expression = "3"
    self.bc_fixture.negate_num()
    assert self.bc_fixture.expression == "-3"

  def test_negate_num_no_num_neg_1(self):
    '''Negate the number before the number is entered (at the start of the expression) with a negative present'''
    self.bc_fixture.expression = "-"
    self.bc_fixture.negate_num()
    assert self.bc_fixture.expression == ""

  def test_negate_num_no_num_neg_2(self):
    '''Negate the number before the number is entered (at the end of the expression) with a negative present'''
    self.bc_fixture.expression = "3+-"
    self.bc_fixture.negate_num()
    assert self.bc_fixture.expression == "3+"

  def test_negate_num_num_neg(self):
    '''Negate the number after the number is entered with a negative present'''
    self.bc_fixture.expression = "-3"
    self.bc_fixture.negate_num()
    assert self.bc_fixture.expression == "3"

  def test_negate_num_decimal_after_num_no_neg(self):
    '''Negate the number with a trailing decimal point without a negative present'''
    self.bc_fixture.expression = "3."
    self.bc_fixture.negate_num()
    assert self.bc_fixture.expression == "-3."

  def test_negate_num_decimal_before_num_no_neg(self):
    '''Negate the number with a leading decimal point without a negative present'''
    self.bc_fixture.expression = ".3"
    self.bc_fixture.negate_num()
    assert self.bc_fixture.expression == "-.3"

  def test_negate_num_decimal_between_num_no_neg(self):
    '''Negate the number with a decimal point within the number without a negative present'''
    self.bc_fixture.expression = "3.5"
    self.bc_fixture.negate_num()
    assert self.bc_fixture.expression == "-3.5"

  def test_negate_num_decimal_after_num_neg(self):
    '''Negate the number with a trailing decimal point with a negative present'''
    self.bc_fixture.expression = "-3."
    self.bc_fixture.negate_num()
    assert self.bc_fixture.expression == "3."

  def test_negate_num_decimal_before_num_neg(self):
    '''Negate the number with a leading decimal point with a negative present'''
    self.bc_fixture.expression = "-.3"
    self.bc_fixture.negate_num()
    assert self.bc_fixture.expression == ".3"

  def test_negate_num_decimal_between_num_neg(self):
    '''Negate the number with a decimal point within the number with a negative present'''
    self.bc_fixture.expression = "-3.5"
    self.bc_fixture.negate_num()
    assert self.bc_fixture.expression == "3.5"


class TestUpdateEqn:
  '''
  Test the BasicCalc.update_eqn function.

  Excluded Test Cases:
    None
  '''
  @pytest.fixture(autouse=True)
  def bc_fixture(self):
    '''A simulated BasicCalc object'''
    self.bc_fixture = BasicCalc(tk.Tk(), tk.Frame())

  def test_update_eqn_number_1(self):
    '''Add a number to an empty expression'''
    self.bc_fixture.expression = ""
    self.bc_fixture.update_eqn(3)
    assert self.bc_fixture.expression == "3"

  def test_update_eqn_number_2(self):
    '''Add a number to an expression that ends in a number'''
    self.bc_fixture.expression = "5"
    self.bc_fixture.update_eqn(3)
    assert self.bc_fixture.expression == "53"

  def test_update_eqn_number_3(self):
    '''Add a number to an expression that ends in an operator'''
    self.bc_fixture.expression = "5+"
    self.bc_fixture.update_eqn(3)
    assert self.bc_fixture.expression == "5+3"

  def test_update_eqn_number_4(self):
    '''Add a number to an expression that ends in a decimal'''
    self.bc_fixture.expression = "0."
    self.bc_fixture.update_eqn(3)
    assert self.bc_fixture.expression == "0.3"

  def test_update_eqn_number_5(self):
    '''Add a number to an expression that ends in a negative sign'''
    self.bc_fixture.expression = "-"
    self.bc_fixture.update_eqn(3)
    assert self.bc_fixture.expression == "-3"

  def test_update_eqn_operator_1(self):
    '''Add an operator to an empty expression'''
    self.bc_fixture.expression = ""
    self.bc_fixture.update_eqn("+")
    assert self.bc_fixture.expression == "0+"

  def test_update_eqn_operator_2(self):
    '''Add an operator to an expression that ends in a number'''
    self.bc_fixture.expression = "3"
    self.bc_fixture.update_eqn("+")
    assert self.bc_fixture.expression == "3+"

  def test_update_eqn_operator_3(self):
    '''Add an operator to an expression that ends in an operator'''
    self.bc_fixture.expression = "3*"
    self.bc_fixture.update_eqn("+")
    assert self.bc_fixture.expression == "3+"

  def test_update_eqn_operator_4(self):
    '''Add an operator to an expression that ends in a decimal'''
    self.bc_fixture.expression = "3."
    self.bc_fixture.update_eqn("+")
    assert self.bc_fixture.expression == "3.+"

  def test_update_eqn_operator_5(self):
    '''Add an operator to an expression that ends in a negative sign'''
    self.bc_fixture.expression = "3*-"
    self.bc_fixture.update_eqn("+")
    assert self.bc_fixture.expression == "3+-"

  def test_update_eqn_decimal_1(self):
    '''Add a decimal point to an empty expression'''
    self.bc_fixture.expression = ""
    self.bc_fixture.update_eqn(".")
    assert self.bc_fixture.expression == "0."

  def test_update_eqn_decimal_2(self):
    '''Add a decimal point to an expression that ends in a number'''
    self.bc_fixture.expression = "3"
    self.bc_fixture.update_eqn(".")
    assert self.bc_fixture.expression == "3."

  def test_update_eqn_decimal_3(self):
    '''Add a decimal point to an expression that ends in an operator'''
    self.bc_fixture.expression = "3+"
    self.bc_fixture.update_eqn(".")
    assert self.bc_fixture.expression == "3+0."

  def test_update_eqn_decimal_4(self):
    '''Add a decimal point to an expression that already contains a decimal point'''
    self.bc_fixture.expression = "3.3"
    self.bc_fixture.update_eqn(".")
    assert self.bc_fixture.expression == "3.3"

  def test_update_eqn_decimal_5(self):
    '''Add a decimal point to an expression that ends in a negative sign'''
    self.bc_fixture.expression = "3+-"
    self.bc_fixture.update_eqn(".")
    assert self.bc_fixture.expression == "3+-0."

  def test_update_eqn_decimal_6(self):
    '''Add a decimal point to an expression with multiple decimal numbers'''
    self.bc_fixture.expression = "3.3+6"
    self.bc_fixture.update_eqn(".")
    assert self.bc_fixture.expression == "3.3+6."

  def test_update_eqn_total_flag_1(self):
    '''Add a number to an expression that is a previous total'''
    self.bc_fixture.expression = "36"
    self.bc_fixture.total_flag = True
    self.bc_fixture.update_eqn("7")
    assert self.bc_fixture.expression == "7" and self.bc_fixture.total_flag == False

  def test_update_eqn_total_flag_2(self):
    '''Add an operator to an expression that is a previous total'''
    self.bc_fixture.expression = "36"
    self.bc_fixture.total_flag = True
    self.bc_fixture.update_eqn("+")
    assert self.bc_fixture.expression == "36+" and self.bc_fixture.total_flag == False

  def test_update_eqn_total_flag_3(self):
    '''Add a decimal point to an expression that is a previous total'''
    self.bc_fixture.expression = "36"
    self.bc_fixture.total_flag = True
    self.bc_fixture.update_eqn(".")
    assert self.bc_fixture.expression == "0." and self.bc_fixture.total_flag == False


class TestSolveEqn:
  '''
  Test the BasicCalc.solve_eqn function.

  Excluded Test Cases:
    None
  '''
  @pytest.fixture(autouse=True)
  def bc_fixture(self):
    '''A simulated BasicCalc object'''
    self.bc_fixture = BasicCalc(tk.Tk(), tk.Frame())

  def test_solve_eqn_empty(self):
    '''Solve the equation when the expression is empty'''
    self.bc_fixture.expression = ""
    self.bc_fixture.solve_eqn(None)
    assert self.bc_fixture.expression == "" and self.bc_fixture.equation.get() == "" and self.bc_fixture.total_flag == False

  def test_solve_eqn_simple(self):
    '''Solve the equation when the expression is a simple integer arithmetic'''
    self.bc_fixture.expression = "3+3"
    self.bc_fixture.solve_eqn(None)
    assert self.bc_fixture.expression == "6" and self.bc_fixture.equation.get() == "6" and self.bc_fixture.total_flag == True

  def test_solve_eqn_division(self):
    '''Solve the equation when the expression is an integer division with an integer result'''
    self.bc_fixture.expression = "6/3"
    self.bc_fixture.solve_eqn(None)
    assert self.bc_fixture.expression == "2" and self.bc_fixture.equation.get() == "2" and self.bc_fixture.total_flag == True

  def test_solve_eqn_division_decimal(self):
    '''Solve the equation when the expression is an integer division with a decimal result'''
    self.bc_fixture.expression = "5/2"
    self.bc_fixture.solve_eqn(None)
    assert self.bc_fixture.expression == "2.5" and self.bc_fixture.equation.get() == "2.5" and self.bc_fixture.total_flag == True

  def test_solve_eqn_division_repeating_decimal(self):
    '''Solve the equation when the expression results in a repeating decimal that should be rounded up'''
    self.bc_fixture.expression = "2/3"
    self.bc_fixture.solve_eqn(None)
    assert self.bc_fixture.expression == "0.666666666666667" and self.bc_fixture.equation.get() == "0.666666666666667" and self.bc_fixture.total_flag == True

  def test_solve_eqn_divide_by_zero(self):
    '''Solve the equation when the expression is a division by zero'''
    self.bc_fixture.expression = "2/0"
    self.bc_fixture.solve_eqn(None)
    assert self.bc_fixture.expression == "" and self.bc_fixture.equation.get() == " NaN " and self.bc_fixture.total_flag == False

  def test_solve_eqn_invalid_modulus(self):
    '''Solve the equation when the expression is in invalid modulus operation'''
    self.bc_fixture.expression = "2%0"
    self.bc_fixture.solve_eqn(None)
    assert self.bc_fixture.expression == "" and self.bc_fixture.equation.get() == " NaN " and self.bc_fixture.total_flag == False

  def test_solve_eqn_invalid_equation(self):
    '''Solve the equation when the expression is in invalid modulus operation'''
    self.bc_fixture.expression = "2+"
    self.bc_fixture.solve_eqn(None)
    assert self.bc_fixture.expression == "" and self.bc_fixture.equation.get() == " NaN " and self.bc_fixture.total_flag == False

