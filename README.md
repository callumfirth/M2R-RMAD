# M2R-RMAD

Vague Todo List:

Paper:
1. Tidy up first 2 sections
2. Create table for example in Section 5.1
3. Tidy up and expand section 5
4. Fnish Section 6
5. Show results from the implementation, specifically compare time taken
7. Move taylor stuff to later on, perhaps after implementation. 

Implementation:
1. Check/Fix to work properly with NumPy arrays (Probably would need to modify reversemode for each output arr)
2. Check to see if traversal of shared expr works properly (As in does x^2 + sin(x^2) have the same operand and only viewed once)
3. Check if the calling Sin() and Cos() wont mess up this 
4. If all previous done and enough time, start to try and implement Matrix multiplication as Ax. Would be like sin and only take one operand which is x. And the operator will have a value A that it applies to? Can do this as we dont care about the adjoint of A?
