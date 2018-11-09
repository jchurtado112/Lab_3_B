#Jesus Hurtado, CS 2302 - Data Structures, Fall 2018, TR: 10:30am - 11:50am
#Create a data structure called engish words by using either a Red-Black Tree
# or an AVL tree, depending on what the user wants. Then, input a word to check 
# if it is a valid word in the english language and create anagrams of that word.
 
class RBTNode:    #Node class for Red-Black Tree
    def __init__(self, key, parent, is_red = False, left = None, right = None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent
        
        if is_red:
            self.color = "red"
        else:
            self.color = "black"

    # Returns true if both child nodes are black. A child set to None is considered
    # to be black.
    def are_both_children_black(self):
        if self.left != None and self.left.is_red():
            return False
        if self.right != None and self.right.is_red():
            return False
        return True

    def count(self):
        count = 1
        if self.left != None:
            count = count + self.left.count()
        if self.right != None:
            count = count + self.right.count()
        return count
    
    # Returns the grandparent of this node
    def get_grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    # Gets this node's predecessor from the left child subtree
    # Precondition: This node's left child is not None
    def get_predecessor(self):
        node = self.left
        while node.right is not None:
            node = node.right
        return node

    # Returns this node's sibling, or None if this node does not have a sibling
    def get_sibling(self):
        if self.parent is not None:
            if self is self.parent.left:
                return self.parent.right
            return self.parent.left
        return None

    # Returns the uncle of this node
    def get_uncle(self):
        grandparent = self.get_grandparent()
        if grandparent is None:
            return None
        if grandparent.left is self.parent:
            return grandparent.right
        return grandparent.left

    # Returns True if this node is black, False otherwise
    def is_black(self):
        return self.color == "black"

    # Returns True if this node is red, False otherwise
    def is_red(self):
        return self.color == "red"

    # Replaces one of this node's children with a new child
    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)
        return False

    # Sets either the left or right child of this node
    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False
            
        if which_child == "left":
            self.left = child
        else:
            self.right = child

        if child != None:
            child.parent = self

        return True


class RedBlackTree:  #Class for the Red-Black Tree
    def __init__(self):
        self.root = None
    
    def __len__(self):
        if self.root is None:
            return 0
        return self.root.count()
    
    def _bst_remove(self, key):    #Go to Remove node function if key is found
        node = self.search(key)
        self._bst_remove_node(node)

    def _bst_remove_node(self, node):   #Remove node
        if node is None:
            return

        # Case 1: Internal node with 2 children
        if node.left is not None and node.right is not None:
            # Find successor
            successor_node = node.right
            while successor_node.left is not None:
                successor_node = successor_node.left

            # Copy successor's key
            successor_key = successor_node.key

            # Recursively remove successor
            self._bst_remove_node(successor_node)

            # Set node's key to copied successor key
            node.key = successor_key

        # Case 2: Root node (with 1 or 0 children)
        elif node is self.root:
            if node.left is not None:
                self.root = node.left
            else:
                self.root = node.right
                    
            # Make sure the new root, if not None, has parent set to None
            if self.root is not None:
                self.root.parent = None
                    
        # Case 3: Internal with left child only
        elif node.left is not None:
            node.parent.replace_child(node, node.left)
                
        # Case 4: Internal with right child OR leaf
        else:
            node.parent.replace_child(node, node.right)

    # Returns the height of this tree
    def get_height(self):
        return self._get_height_recursive(self.root)

    def _get_height_recursive(self, node):
        if node is None:
            return -1
        left_height = self._get_height_recursive(node.left)
        right_height = self._get_height_recursive(node.right)
        return 1 + max(left_height, right_height)
    
    def insert(self, key):
        new_node = RBTNode(key, None, True, None, None)
        self.insert_node(new_node)
        
    def insert_node(self, node):
        # Begin with normal BST insertion
        if self.root is None:
            # Special case for root
            self.root = node
        else:
            current_node = self.root
            while current_node is not None:
                if node.key < current_node.key:
                    if current_node.left is None:
                        current_node.set_child("left", node)
                        break
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.set_child("right", node)
                        break
                    else:
                        current_node = current_node.right
        
        # Color the node red
        node.color = "red"
            
        # Balance
        self.insertion_balance(node)

    def insertion_balance(self, node):
        # If node is the tree's root, then color node black and return
        if node.parent is None:
            node.color = "black"
            return
        
        # If parent is black, then return without any alterations
        if node.parent.is_black():
            return
    
        # References to parent, grandparent, and uncle are needed for remaining operations
        parent = node.parent
        grandparent = node.get_grandparent()
        uncle = node.get_uncle()
        
        # If parent and uncle are both red, then color parent and uncle black, color grandparent
        # red, recursively balance  grandparent, then return
        if uncle is not None and uncle.is_red():
            parent.color = uncle.color = "black"
            grandparent.color = "red"
            self.insertion_balance(grandparent)
            return

        # If node is parent's right child and parent is grandparent's left child, then rotate left
        # at parent, update node and parent to point to parent and grandparent, respectively
        if node is parent.right and parent is grandparent.left:
            self.rotate_left(parent)
            node = parent
            parent = node.parent
        # Else if node is parent's left child and parent is grandparent's right child, then rotate
        # right at parent, update node and parent to point to parent and grandparent, respectively
        elif node is parent.left and parent is grandparent.right:
            self.rotate_right(parent)
            node = parent
            parent = node.parent

        # Color parent black and grandparent red
        parent.color = "black"
        grandparent.color = "red"
                
        # If node is parent's left child, then rotate right at grandparent, otherwise rotate left
        # at grandparent
        if node is parent.left:
            self.rotate_right(grandparent)
        else:
            self.rotate_left(grandparent)

    # Performs an in-order traversal, calling the visitor function for each node in the tree
    def in_order(self, visitor_function):
        self.in_order_recursive(visitor_function, self.root)

    # Performs an in-order traversal
    def in_order_recursive(self, visitor_function, node):
        if node is None:
            return
        # Left subtree, then node, then right subtree
        self.in_order_recursive(visitor_function, node.left)
        visitor_function(node)
        self.in_order_recursive(visitor_function, node.right)

    def is_none_or_black(self, node):   #Checks if its none or black
        if node is None:
            return True
        return node.is_black()

    def is_not_none_and_red(self, node):   #Checks if its none and red
        if node is None:
            return False
        return node.is_red()

    def prepare_for_removal(self, node):
        if self.try_case1(node):
            return

        sibling = node.get_sibling()
        if self.try_case2(node, sibling):
            sibling = node.get_sibling()
        if self.try_case3(node, sibling):
            return
        if self.try_case4(node, sibling):
            return
        if self.try_case5(node, sibling):
            sibling = node.get_sibling()
        if self.try_case6(node, sibling):
            sibling = node.get_sibling()

        sibling.color = node.parent.color
        node.parent.color = "black"
        if node is node.parent.left:
            sibling.right.color = "black"
            self.rotate_left(node.parent)
        else:
            sibling.left.color = "black"
            self.rotate_right(node.parent)

    def remove(self, key):
        node = self.search(key)
        if node is not None:
            self.remove_node(node)
            return True
        return False

    def remove_node(self, node):
        if node.left is not None and node.right is not None:
            predecessor_node = node.get_predecessor()
            predecessor_key = predecessor_node.key
            self.remove_node(predecessor_node)
            node.key = predecessor_key
            return

        if node.is_black():
            self.prepare_for_removal(node)
        self._bst_remove(node.key)

        # One special case if the root was changed to red
        if self.root is not None and self.root.is_red():
            self.root.color = "black"

    def rotate_left(self, node):
        right_left_child = node.right.left
        if node.parent != None:
            node.parent.replace_child(node, node.right)
        else: # node is root
            self.root = node.right
            self.root.parent = None
        node.right.set_child("left", node)
        node.set_child("right", right_left_child)

    def rotate_right(self, node):
        left_right_child = node.left.right
        if node.parent != None:
            node.parent.replace_child(node, node.left)
        else: # node is root
            self.root = node.left
            self.root.parent = None
        node.left.set_child("right", node)
        node.set_child("left", left_right_child)
            
    def search(self, key):
        current_node = self.root
        while current_node is not None:
            # Return the node if the key matches.
            if current_node.key == key:
                return current_node
                
            # Navigate to the left if the search key is
            # less than the node's key.
            elif key < current_node.key:
                current_node = current_node.left

            # Navigate to the right if the search key is
            # greater than the node's key.
            else:
                current_node = current_node.right

        # The key was not found in the tree.
        return None

    def try_case1(self, node):
        if node.is_red() or node.parent is None:
            return True
        return False # node case 1

    def try_case2(self, node, sibling):
        if sibling.is_red():
            node.parent.color = "red"
            sibling.color = "black"
            if node is node.parent.left:
                self.rotate_left(node.parent)
            else:
                self.rotate_right(node.parent)
            return True
        return False # not case 2

    def try_case3(self, node, sibling):
        if node.parent.is_black() and sibling.are_both_children_black():
            sibling.color = "red"
            self.prepare_for_removal(node.parent)
            return True
        return False # not case 3

    def try_case4(self, node, sibling):
        if node.parent.is_red() and sibling.are_both_children_black():
            node.parent.color = "black"
            sibling.color = "red"
            return True
        return False # not case 4

    def try_case5(self, node, sibling):
        if self.is_not_none_and_red(sibling.left) and self.is_none_or_black(sibling.right) and node is node.parent.left:
            sibling.color = "red"
            sibling.left.color = "black"
            self.rotate_right(sibling)
            return True
        return False # not case 5

    def try_case6(self, node, sibling):
        if self.is_none_or_black(sibling.left) and self.is_not_none_and_red(sibling.right) and node is node.parent.right:
            sibling.color = "red"
            sibling.right.color = "black"
            self.rotate_left(sibling)
            return True
        return False # not case 6
    
def _pretty_tree_helper(root, curr_index=0):
    if root is None:
        return [], 0, 0, 0

    line1 = []
    line2 = []
    node_repr = str(root.key)

    new_root_width = gap_size = len(node_repr)
    
    # Get the left and right sub-boxes, their widths, and root repr positions
    l_box, l_box_width, l_root_start, l_root_end = _pretty_tree_helper(root.left, 2 * curr_index + 1)
    r_box, r_box_width, r_root_start, r_root_end = _pretty_tree_helper(root.right, 2 * curr_index + 2)

    # Draw the branch connecting the current root to the left sub-box
    # Pad with whitespaces where necessary
    
    if l_box_width > 0:
        l_root = (l_root_start + l_root_end) // 2 + 1
        line1.append(' ' * (l_root + 1))
        line1.append('_' * (l_box_width - l_root))
        line2.append(' ' * l_root + '/')
        line2.append(' ' * (l_box_width - l_root))
        new_root_start = l_box_width + 1
        gap_size += 1
    else:
        new_root_start = 0

    # Draw the representation of the current root
    
    line1.append(node_repr)
    line2.append(' ' * new_root_width)

    # Draw the branch connecting the current root to the right sub-box
    # Pad with whitespaces where necessary
    
    if r_box_width > 0:
        r_root = (r_root_start + r_root_end) // 2
        line1.append('_' * r_root)
        line1.append(' ' * (r_box_width - r_root + 1))
        line2.append(' ' * r_root + '\\')
        line2.append(' ' * (r_box_width - r_root))
        gap_size += 1
    new_root_end = new_root_start + new_root_width - 1

    # Combine the left and right sub-boxes with the branches drawn above
    
    gap = ' ' * gap_size
    new_box = [''.join(line1), ''.join(line2)]
    for i in range(max(len(l_box), len(r_box))):
        l_line = l_box[i] if i < len(l_box) else ' ' * l_box_width
        r_line = r_box[i] if i < len(r_box) else ' ' * r_box_width
        new_box.append(l_line + gap + r_line)

    # Return the new box, its width and its root positions
    return new_box, len(new_box[0]), new_root_start, new_root_end
    
def pretty_tree(tree):
    lines = _pretty_tree_helper(tree.root, 0)[0]
    return '\n' + '\n'.join((line.rstrip() for line in lines))

class Node:
    
    # Constructor with a key parameter creates the Node object.
    
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0
        
    # Method to calculate the current nodes's balance factor node, 
    # defined as height(left subtree) - height(right subtree)
    
    def get_balance(self):
        # Get current height of left subtree, or -1 if None
        left_height = -1
        if self.left is not None:
            left_height = self.left.height
            
        # Get right subtree's current height, or -1 if None
        right_height = -1
        if self.right is not None:
            right_height = self.right.height
            
        # Calculate the balance factor.
        return left_height - right_height

    # Recalculates the current height of the subtree rooted at
    # the node, usually called after a subtree has been 
    # modified.
    
    def update_height(self):
        # Get current height of left subtree, or -1 if None
        left_height = -1
        if self.left is not None:
            left_height = self.left.height
            
        # Get current height of right subtree, or -1 if None
        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        # Assign self.height with calculated node height.
        self.height = max(left_height, right_height) + 1

        
    # Assign either the left or right data member with a new
    # child. The parameter which_child is expected to be the
    # string "left" or the string "right". Returns True if
    # the new child is successfully assigned to this node, False
    # otherwise.
    
    def set_child(self, which_child, child):
        # Ensure which_child is properly assigned.
        if which_child != "left" and which_child != "right":
            return False

        # Assign the left or right data member.
        if which_child == "left":
            self.left = child
        else:
            self.right = child

        # Assign the new child's parent data member,
        # if the child is not None.
        if child is not None:
            child.parent = self

        # Update the node's height, since the structure
        # of the subtree may have changed.
        self.update_height()
        return True

    # Replace a current child with a new child. Determines if
    # the current child is on the left or right, and calls
    # set_child() with the new node appropriately.
    # Returns True if the new child is assigned, False otherwise.
    
    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)
          
        # If neither of the above cases applied, then the new child
        # could not be attached to this node.
        return False

        
class AVLTree:
    def __init__(self):
        # Constructor to create an empty AVLTree. There is only
        # one data member, the tree's root Node, and it starts
        # out as None.
        self.root = None

    # Performs a left rotation at the given node. Returns the
    # subtree's new root.
    def rotate_left(self, node):
        # Define a convenience pointer to the right child of the 
        # left child.
        right_left_child = node.right.left
        
        # Step 1 - the right child moves up to the node's position.
        # This detaches node from the tree, but it will be reattached
        # later.
        if node.parent is not None:
            node.parent.replace_child(node, node.right)
        else:  # node is root
            self.root = node.right
            self.root.parent = None

        # Step 2 - the node becomes the left child of what used
        # to be its right child, but is now its parent. This will
        # detach right_left_child from the tree.
        node.right.set_child('left', node)
        
        # Step 3 - reattach right_left_child as the right child of node.
        node.set_child('right', right_left_child)
        
        return node.parent

    # Performs a right rotation at the given node. Returns the
    # subtree's new root.
    def rotate_right(self, node):
        # Define a convenience pointer to the left child of the 
        # right child.
        left_right_child = node.left.right
        
        # Step 1 - the left child moves up to the node's position.
        # This detaches node from the tree, but it will be reattached
        # later.
        if node.parent is not None:
            node.parent.replace_child(node, node.left)
        else:  # node is root
            self.root = node.left
            self.root.parent = None

        # Step 2 - the node becomes the right child of what used
        # to be its left child, but is now its parent. This will
        # detach left_right_child from the tree.
        node.left.set_child('right', node)

        # Step 3 - reattach left_right_child as the left child of node.
        node.set_child('left', left_right_child)
        
        return node.parent

    # Updates the given node's height and rebalances the subtree if
    # the balancing factor is now -2 or +2. Rebalancing is done by
    # performing a rotation. Returns the subtree's new root if
    # a rotation occurred, or the node if no rebalancing was required.
    def rebalance(self, node):
    
        # First update the height of this node.
        node.update_height()        
        
        # Check for an imbalance.
        if node.get_balance() == -2:
        
            # The subtree is too big to the right.
            if node.right.get_balance() == 1:
                # Double rotation case. First do a right rotation
                # on the right child.
                self.rotate_right(node.right)
                
            # A left rotation will now make the subtree balanced.
            return self.rotate_left(node)
                        
        elif node.get_balance() == 2:

            # The subtree is too big to the left
            if node.left.get_balance() == -1:
                # Double rotation case. First do a left rotation
                # on the left child.
                self.rotate_left(node.left)
                
            # A right rotation will now make the subtree balanced.
            return self.rotate_right(node)
            
        # No imbalance, so just return the original node.
        return node

    # Insert a new node into the AVLTree. When insert() is complete,
    # the AVL tree will be balanced.
    
    def insert(self, node):
        
        # Special case: if the tree is empty, just set the root to
        # the new node.
        if self.root is None:
            self.root = node
            node.parent = None

        else:
            # Step 1 - do a regular binary search tree insert.
            current_node = self.root
            while current_node is not None:
                # Choose to go left or right
                if node.key < current_node.key:
                    # Go left. If left child is None, insert the new
                    # node here.
                    if current_node.left is None:
                        current_node.left = node
                        node.parent = current_node
                        current_node = None
                    else:
                        # Go left and do the loop again.
                        current_node = current_node.left
                else:
                    # Go right. If the right child is None, insert the
                    # new node here.
                    if current_node.right is None:
                        current_node.right = node
                        node.parent = current_node
                        current_node = None
                    else:
                        # Go right and do the loop again.
                        current_node = current_node.right
            
            # Step 2 - Rebalance along a path from the new node's parent up
            # to the root.
            node = node.parent
            while node is not None:
                self.rebalance(node)
                node = node.parent

    # Searches for a node with a matching key. Does a regular
    # binary search tree search operation. Returns the node with the
    # matching key if it exists in the tree, or None if there is no
    # matching key in the tree.
    
    def search(self, key):
        current_node = self.root
        while current_node is not None:
            # Compare the current node's key with the target key.
            # If it is a match, return the current key; otherwise go
            # either to the left or right, depending on whether the 
            # current node's key is smaller or larger than the target key.
            if current_node.key == key: return current_node
            elif current_node.key < key: current_node = current_node.right
            else: current_node = current_node.left

    # Attempts to remove a node with a matching key. If no node has a matching key
    # then nothing is done and False is returned; otherwise the node is removed and
    # True is returned.
    
    def remove_key(self, key):
        node = self.search(key)
        if node is None:
            return False
        else:
            return self.remove_node(node)
            
    # Removes the given node from the tree. The left and right subtrees,
    # if they exist, will be reattached to the tree such that no imbalances
    # exist, and the binary search tree property is maintained. Returns True
    # if the node is found and removed, or False if the node is not found in
    # the tree.es return after directly removing the node.
    
    def remove_node(self, node):
        # Base case: 
        if node is None:
            return False
            
        # Parent needed for rebalancing.
        parent = node.parent
            
        # Case 1: Internal node with 2 children
        if node.left is not None and node.right is not None:
            # Find successor
            successor_node = node.right
            while successor_node.left != None:
                successor_node = successor_node.left
                
            # Copy the value from the node
            node.key = successor_node.key
                
            # Recursively remove successor
            self.remove_node(successor_node)
                
            # Nothing left to do since the recursive call will have rebalanced
            return True
        
        # Case 2: Root node (with 1 or 0 children)
        elif node is self.root:
            if node.left is not None:
                 self.root = node.left
            else:
                 self.root = node.right

            if self.root is not None:
                 self.root.parent = None

            return True
        
        # Case 3: Internal with left child only
        elif node.left is not None:
            parent.replace_child(node, node.left)
            
        # Case 4: Internal with right child only OR leaf
        else:
            parent.replace_child(node, node.right)
            
        # node is gone. Anything that was below node that has persisted is already correctly
        # balanced, but ancestors of node may need rebalancing.
        node = parent
        while node is not None:
            self.rebalance(node)            
            node = node.parent
        
        return True
        
    # Overloading the __str__() operator to create a nicely-formatted text representation of
    # the tree. Derived from Joohwan Oh at: 
    #    https://github.com/joowani/binarytree/blob/master/binarytree/__init__.py
    
    def __str__(self):
        return pretty_tree(self)


def print_anagrams(word, prefix=""): #Print anagrams method
    if len(word) <= 1:
        strr = prefix + word
        if engish_words.search(strr):##str in engish_words: 
            print(prefix + word)
            
    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i] # letters before cur 
            after = word[i + 1:] # letters after cur
            
            if cur not in before: # Check if permutations of cur have not been generated. 
                print_anagrams(before + after, prefix + cur)
               

def count_anagrams(counter,tree,word,prefix=""): #Count anagrams method
    if len(word) <= 1:
        strr = prefix + word
        if tree.search(strr): ##str in engish_words: 
            counter +=1
    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i] # letters before cur 
            after = word[i + 1:] # letters after cur
            if cur not in before: # Check if permutations of cur have not been generated.   
                counter = count_anagrams(counter,tree,before + after, prefix + cur) 
    return counter                 

def greatest_anagrams(file,tree):
    #Initializes the variables used to determine greatest anagrams
    counter = -1
    max_anagrams = -1
    max_word = ''
    
    f = open(file)  #Reads the file and saves all lines
    list_of_words = f.readlines()
    
    for i in range(len(list_of_words)): #Creates an array to store each word
        list_of_words[i] = list_of_words[i][:-1]
    if tree == 'AVL':
        new_tree = AVLTree()    #Creates an AVL object
        for ln in list_of_words:
            words = Node(ln)    #Stores each word into a node of the AVL implementation
            new_tree.insert(words) 
    if tree  == 'RBT':
        new_tree = RedBlackTree()   #Creates a Red-Black object
        for ln in list_of_words:
            new_tree.insert(ln) #Inserts each line into RB implementation
            
    for word in list_of_words:  #Iterates through each word and checks how many anagrams each word has
        counter = count_anagrams(0,new_tree,word)
        if(counter > max_anagrams):
            max_anagrams = counter
            max_word = word     #Will save the word with greatest anagram found
    
    #Prints word with greatest anagram
    print("Word with most anagrams is: {}, anagrams: {}".format(max_word,max_anagrams))      
    
#Get content from file
content= open("my_words.txt")
word_list = content.readlines()

#User is given the choice to use either Red_Black or AVL Tree implementation
get_tree = input("How would you like to implement your Data Structure?, AVL ('AVL') or Red-Black Tree ('RBT')?  ")  

if get_tree == 'AVL':   #If user inputs AVL, engish_word will be implemented using an AVL Tree
    engish_words = AVLTree()
    for ln in word_list:
        ln = ln.replace('\n','')
        words = Node(ln)
        engish_words.insert(words)
    
if get_tree  == 'RBT':  #If user inputs RBT, engish_word will be created using a Red_black Tree
    engish_words = RedBlackTree()
    for ln in word_list:
        ln = ln.replace('\n','')
        engish_words.insert(ln)

#Asks user to input a word, then prints anagrams of the word and number of anagrams 
word = input("Input a word to create anagrams: ")
print_anagrams(word)
count = count_anagrams(0,engish_words,word)
print("Number of anagrams = ",count)

#Checks which word in file has greatest anagram
greatest_anagrams('my_words.txt',get_tree)