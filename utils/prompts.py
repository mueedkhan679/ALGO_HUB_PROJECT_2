"""
System Prompts and Templates
Contains the system prompt and other prompt templates for the chatbot
"""

# Main system prompt for the e-commerce support chatbot
SYSTEM_PROMPT = """You are a helpful, polite, and professional E-commerce Customer Support Assistant for ShopEase, a leading online retail store. Your role is to assist customers with their inquiries about orders, returns, products, and general shopping experience.

## Core Responsibilities:
1. **Order Tracking**: Help customers track their orders using their Order ID. You can provide estimated delivery dates and current shipping status.
2. **Return & Refund Policy**: Explain our 30-day return policy clearly. Customers can return items within 30 days of delivery for a full refund or exchange.
3. **Product Queries**: Answer questions about product availability, specifications, sizing, and recommendations.
4. **General Support**: Assist with account issues, payment methods, shipping options, and other customer service matters.

## Company Policies to Remember:
- **Return Policy**: 30-day hassle-free returns from the date of delivery
- **Order Tracking**: Customers need their Order ID (format: SE-XXXXXX) to track orders
- **Shipping**: Standard shipping (5-7 business days), Express shipping (2-3 business days)
- **Refund Processing**: Refunds are processed within 5-7 business days after we receive the returned item
- **Customer Service Hours**: Monday-Friday, 9 AM - 6 PM EST
- **Contact Escalation**: For complex issues requiring human intervention, politely direct customers to contact support@shopease.com or call 1-800-SHOP-EASE

## Communication Guidelines:
- Always be polite, empathetic, and patient
- Use clear, simple language - avoid jargon
- If you don't know the answer, be honest and offer to connect them with a human agent
- Never make promises about delivery dates or refunds that you can't guarantee
- Always ask for the Order ID when helping with order-related issues
- Confirm understanding by summarizing the customer's issue before providing solutions

## Response Format:
- Keep responses concise but thorough (2-4 paragraphs maximum)
- Use bullet points for lists when appropriate
- Include relevant links or contact information when needed
- End with a follow-up question to ensure customer satisfaction

Remember: Your goal is to provide excellent customer service that makes shopping at ShopEase a delightful experience!
"""

# Prompt template for order tracking
ORDER_TRACKING_TEMPLATE = """
The customer is asking about order tracking. Their Order ID is: {order_id}

Please provide:
1. Current order status
2. Estimated delivery date
3. Shipping carrier and tracking number (if available)
4. Any delivery instructions or notes

If the Order ID format is invalid or not found, politely ask them to verify their Order ID.
"""

# Prompt template for return policy inquiries
RETURN_POLICY_TEMPLATE = """
The customer is asking about returns or refunds. Their concern is: {customer_concern}

Please explain:
1. Our 30-day return policy
2. The return process step-by-step
3. Refund timeline (5-7 business days after we receive the item)
4. Any conditions or exceptions
5. How to initiate a return

Be empathetic if they seem frustrated and offer to help them start the return process.
"""

# Prompt template for product queries
PRODUCT_QUERY_TEMPLATE = """
The customer is asking about a product. Their question is: {product_question}

Please provide:
1. Product information and specifications
2. Availability status
3. Pricing information (if applicable)
4. Similar product recommendations if the requested item is unavailable
5. Size guides or care instructions if relevant

If you don't have specific product information, direct them to the product page or offer to check with the inventory team.
"""

# Prompt template for escalation
ESCALATION_TEMPLATE = """
The customer's issue requires human intervention. Their concern is: {issue_summary}

Please:
1. Acknowledge their frustration or concern empathetically
2. Explain that you're connecting them with a specialist
3. Provide contact information:
   - Email: support@shopease.com
   - Phone: 1-800-SHOP-EASE (1-800-766-7327)
   - Hours: Monday-Friday, 9 AM - 6 PM EST
4. Assure them that the human agent will have access to their conversation history
5. Thank them for their patience
"""


def get_system_prompt() -> str:
    """
    Get the main system prompt.
    
    Returns:
        The system prompt string
    """
    return SYSTEM_PROMPT


def get_order_tracking_prompt(order_id: str) -> str:
    """
    Get the order tracking prompt template.
    
    Args:
        order_id: The customer's order ID
        
    Returns:
        Formatted order tracking prompt
    """
    return ORDER_TRACKING_TEMPLATE.format(order_id=order_id)


def get_return_policy_prompt(customer_concern: str) -> str:
    """
    Get the return policy prompt template.
    
    Args:
        customer_concern: The customer's specific concern about returns
        
    Returns:
        Formatted return policy prompt
    """
    return RETURN_POLICY_TEMPLATE.format(customer_concern=customer_concern)


def get_product_query_prompt(product_question: str) -> str:
    """
    Get the product query prompt template.
    
    Args:
        product_question: The customer's product-related question
        
    Returns:
        Formatted product query prompt
    """
    return PRODUCT_QUERY_TEMPLATE.format(product_question=product_question)


def get_escalation_prompt(issue_summary: str) -> str:
    """
    Get the escalation prompt template.
    
    Args:
        issue_summary: Summary of the issue requiring human intervention
        
    Returns:
        Formatted escalation prompt
    """
    return ESCALATION_TEMPLATE.format(issue_summary=issue_summary)


def detect_intent(user_message: str) -> str:
    """
    Simple intent detection to route to appropriate prompt template.
    
    Args:
        user_message: The user's message
        
    Returns:
        Intent category: 'order_tracking', 'return_policy', 'product_query', 'general', or 'escalation'
    """
    user_message_lower = user_message.lower()
    
    # Order tracking keywords
    order_keywords = ['track', 'tracking', 'order status', 'where is my order', 'delivery', 'shipping status', 'order id']
    if any(keyword in user_message_lower for keyword in order_keywords):
        return 'order_tracking'
    
    # Return/refund keywords
    return_keywords = ['return', 'refund', 'money back', 'exchange', 'send back', 'cancel order']
    if any(keyword in user_message_lower for keyword in return_keywords):
        return 'return_policy'
    
    # Product keywords
    product_keywords = ['product', 'item', 'available', 'in stock', 'size', 'color', 'price', 'specification']
    if any(keyword in user_message_lower for keyword in product_keywords):
        return 'product_query'
    
    # Escalation keywords (frustration, complaint, etc.)
    escalation_keywords = ['speak to human', 'manager', 'supervisor', 'complaint', 'unacceptable', 'worst service']
    if any(keyword in user_message_lower for keyword in escalation_keywords):
        return 'escalation'
    
    return 'general'