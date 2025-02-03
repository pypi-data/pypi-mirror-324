import ast
def sparta_4ac2b16c3f(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_db7a34de68(script_text):return sparta_4ac2b16c3f(script_text)