from unittest import TestCase
from src.nodes import *
from src.interpreter import Interpreter
from src.values import Number


class TestInterpreter(TestCase):
    
    def test_numbers(self):
        value = Interpreter().visit(NumberNode(51.2))
        self.assertEqual(value, Number(51.2))
    
    def test_individual_operations(self):
        value = Interpreter().visit(AddNode(NumberNode(27), NumberNode(14)))
        self.assertEqual(value, Number(41))
        
        value = Interpreter().visit(SubtractNode(NumberNode(27), NumberNode(14)))
        self.assertEqual(value, Number(13))
        
        value = Interpreter().visit(MultiplyNode(NumberNode(27), NumberNode(14)))
        self.assertEqual(value, Number(378))
        
        value = Interpreter().visit(DivideNode(NumberNode(27), NumberNode(14)))
        self.assertAlmostEqual(value.value, 1.92857, 5)
    
        with self.assertRaises(Exception):
            Interpreter().visit(DivideNode(NumberNode(27), NumberNode(0)))
        
    def test_full_expression(self):
        tree = AddNode(
            NumberNode(27),
            MultiplyNode(
                SubtractNode(
                    DivideNode(
                        NumberNode(43),
                        NumberNode(36)
                    ),
                    NumberNode(48),
                ),
                NumberNode(51)
            )
        )
        
        result =  Interpreter().visit(tree)
        self.assertAlmostEqual(result.value, -2360.08, 2)
        # -2360.08