import graphviz
dot = graphviz.Digraph(comment='The Round Table')
dot.node('1', '*')  
dot.node('2', 'Sin()')
dot.node('3', '4')
dot.node('4', 'Sir Lancelot the Brave')

dot.edges(['31', '31', '12'])
#dot.edge('1', '2', constraint='frue')
print(dot.source)
dot.render('doctest-output/round-table.gv').replace('\\', '/')
dot.render('doctest-output/round-table.gv', view=True)
