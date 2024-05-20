class HTMLNode:
    
    def __init__(self, 
                 tag=None, 
                 value=None, 
                 children=None, 
                 props=None):
        
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props:
            return ' ' + ' '.join([f'{k}="{v}"' for k, v in self.props.items()])
        else:
            return ''
        
    def __repr__(self):
        return f"tag: {self.tag} value: {self.value} children: {self.children} props: {self.props}"
    
class ParentNode(HTMLNode):
    
    def __init__(self,
                 tag,
                 children):
    
        super().__init__(tag=tag,
                        children=children)
    
    def to_html(self):
        if not self.children:
            raise ValueError("children are required")
        if not self.tag:
            raise ValueError("tag is required")
        
        return f"<{self.tag}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"
    
class LeafNode(HTMLNode):
    
    def __init__(self, 
                 tag=None, 
                 value=None, 
                 props=None):
        
        
        super().__init__(tag=tag,
                         value=value,
                         props=props)
        
    def to_html(self):
        html_string = f""
        if self.value:
            html_string = self.value
        if self.tag: 
            html_string = f"<{self.tag}>{html_string}</{self.tag}>"
        if self.props:
            index = html_string.find('>')
            html_string = html_string[:index] + self.props_to_html() + html_string[index:]
        
        return html_string