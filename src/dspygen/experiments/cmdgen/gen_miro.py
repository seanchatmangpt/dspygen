from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Type
from openai import OpenAI

from dspygen.modules.json_module import json_call

client = OpenAI()


# Define the schema for a Miro widget
class Widget(BaseModel):
    id: str = Field(..., description="Descriptive identifier for the widget")
    text: Optional[str] = Field(..., description="The text content of the widget, if applicable")
    color: str = Field(..., description="Hex code of the color.")

    class Config:
        extra = 'allow'  # Allow extra fields


# Define the schema for a Miro line
class Line(BaseModel):
    id: str = Field(..., description="Descriptive identifier for the line")
    start_widget_id: str = Field(..., description="ID of the widget where the line starts")
    end_widget_id: str = Field(..., description="ID of the widget where the line ends")
    color: str = Field(..., description="Hex code of the color of the line")

    class Config:
        extra = 'allow'  # Allow extra fields


# Define the combined response schema
class ResponseWidgets(BaseModel):
    widgets: List[Widget] = Field(None, description="An array of widget objects")


class ResponseLines(BaseModel):
    lines: List[Line] = Field(None, description="An array of line objects")


sys_prompt_widget = f"""You are a Miro board widget generator AI specialized in Elixir and event-sourced systems. 
Your task is to translate the user's domain model, including commands, events, aggregates, projections, 
and process managers, into correctly formatted Miro board widgets. Each widget should be color-coded 
according to its type (e.g., commands, events, projections) and should include relevant details 
such as names and relationships between widgets.

### Widget Color Coding:
- **Aggregates:**
  - **Color:**  (#f5d128)
  - **Description:** Aggregates represent the primary entities or domain objects. They manage state and enforce business rules.

- **Commands:**
  - **Color:**  (#a6ccf5)
  - **Description:** Commands represent actions that initiate changes in the system.

- **Events:**
  - **Color:**  (#ff9d48)
  - **Description:** Events represent state changes in the system, often triggered by commands.

- **Event Handlers:**
  - **Color:** (#ea94bb)
  - **Description:** Event handlers react to specific events and perform side effects or initiate further actions.

- **Process Managers:**
  - **Color:** (#be88c7)
  - **Description:** Process managers handle long-running business processes by reacting to events and issuing commands.

- **Projections:**
  - **Color:** (#d5f692)
  - **Description:** Projections are used to query the current state of the system and are built from events.

### Line Color Coding:
- **Default Line Color:** Black (#000000)

- **Connections:**
  - **Command to Event:** Use a solid line.
  - **Event to Event Handler:** Use a dashed line.
  - **Event to Process Manager:** Use a dotted line.
  - **Event to Projection:** Use a solid line.

"""

sys_prompt_line = f"""You are a Miro board widget generator AI specialized in Elixir and event-sourced systems. 
Your task is to translate the user's domain model, including commands, events, aggregates, projections, 
and process managers, into correctly formatted Miro board lines. 

### Line Color Coding:
- **Default Line Color:** Black (#000000)

- **Connections:**
  - **Command to Event:** Use a solid line.
  - **Event to Event Handler:** Use a dashed line.
  - **Event to Process Manager:** Use a dotted line.
  - **Event to Projection:** Use a solid line.
"""

user_msg_widgets = f"""Generate a Miro board with the following domain model components:
1. **Aggregates:**
   - Auction
   - Item

2. **Commands:**
   - StartAuction
   - PlaceBid

3. **Events:**
   - AuctionStarted
   - BidPlaced
   - BidderOutbid

4. **Event Handlers:**
   - HighestBidderNotifier 
   - OutbidNotifier

5. **Process Managers:**
   - AuctionProcessManager

6. **Projections:**
   - AuctionSummary 
   - ItemSummary 
"""

user_msg_lines = f"""Generate lines for the following connections:

1. **Commands to Events:**
   - Connect "StartAuction" to "AuctionStarted"
   - Connect "PlaceBid" to "BidPlaced"

2. **Events to Event Handlers:**
   - Connect "BidPlaced" to "HighestBidderNotifier"
   - Connect "BidderOutbid" to "OutbidNotifier"

3. **Events to Process Managers:**
   - Connect "AuctionStarted" and "BidPlaced" to "AuctionProcessManager"

4. **Events to Projections:**
   - Connect "AuctionStarted" and "BidPlaced" to "AuctionSummary"
   - Connect "AuctionStarted" and "BidPlaced" to "ItemSummary"
"""


class Message(BaseModel):
    role: str
    content: str


class ChatCompletion(BaseModel):
    model: str
    messages: List[Message]


def get_parsed_response(system_prompt: str,
                        user_message: str,
                        response_format: Type[BaseModel]):
    """
    Function to get parsed response from GPT model

    system_prompt (str): The system prompt
    user_message (str): The user message
    response_format (Type[BaseModel]): The expected response format as a Pydantic model
    """
    system_prompt = f"""{system_prompt}

    # FOLLOW THE JSON SCHEMA EXACTLY
    ```schema
    {response_format.model_json_schema()}
    ```

    # RESPONSE AS JSON
    ```json
    """
    messages = [
        Message(role="system", content=system_prompt),
        Message(role="user", content=user_message)
    ]

    chat_completion = ChatCompletion(
        model="gpt-4o-mini",
        messages=messages,
        response_format=response_format,
    )

    response = client.beta.chat.completions.parse(**chat_completion.model_dump())
    message = response.choices[0].message
    parsed = response.choices[0].message.parsed

    if parsed is None:
        from dspygen.utils.json_tools import extract
        parsed = extract(message.content)

    try:
        model = response_format.model_validate(parsed)
    except ValidationError as e:
        messages.append(Message(role="assistant", content=str(parsed)))
        messages.append(Message(role="user", content=f"{str(e)}\nPlease return the correct json\n```json\n"))

        chat_completion = ChatCompletion(
            model="gpt-4o-mini",
            messages=messages,
            response_format=response_format,
        )

        response = client.beta.chat.completions.parse(**chat_completion.model_dump())
        message = response.choices[0].message
        parsed = response.choices[0].message.parsed

        if parsed is None:
            from dspygen.utils.json_tools import extract
            parsed = extract(message.content)

        model = response_format.model_validate(parsed)

    return model


from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Union


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()

    # # First call: Generate Widgets
    # response_widgets = get_parsed_response(system_prompt=sys_prompt_widget,
    #                                        user_message=user_msg_widgets,
    #                                        response_format=ResponseWidgets)
    # print(response_widgets)
    #
    # msg_lines = f"{response_widgets.model_dump_json()}\n\n{user_msg_lines}"
    #
    # # Second call: Generate Lines
    # response_lines = get_parsed_response(system_prompt=sys_prompt_line,
    #                                      user_message=msg_lines,
    #                                      response_format=ResponseLines)
    # print(response_lines)

    widgets = [Widget(id='aggregate_auction', text='Auction', color='#f5d128'),
               Widget(id='aggregate_item', text='Item', color='#f5d128'),
               Widget(id='command_start_auction', text='StartAuction', color='#a6ccf5'),
               Widget(id='command_place_bid', text='PlaceBid', color='#a6ccf5'),
               Widget(id='event_auction_started', text='AuctionStarted', color='#ff9d48'),
               Widget(id='event_bid_placed', text='BidPlaced', color='#ff9d48'),
               Widget(id='event_bidder_outbid', text='BidderOutbid', color='#ff9d48'),
               Widget(id='event_handler_highest_bidder_notifier', text='HighestBidderNotifier', color='#ea94bb'),
               Widget(id='event_handler_outbid_notifier', text='OutbidNotifier', color='#ea94bb'),
               Widget(id='process_manager_auction', text='AuctionProcessManager', color='#be88c7'),
               Widget(id='projection_auction_summary', text='AuctionSummary', color='#d5f692'),
               Widget(id='projection_item_summary', text='ItemSummary', color='#d5f692'),
               Widget(id='connection_command_to_event_auction_started', text='StartAuction -> AuctionStarted',
                      color='#000000'),
               Widget(id='connection_command_to_event_bid_placed', text='PlaceBid -> BidPlaced', color='#000000'),
               Widget(id='connection_event_to_event_handler_highest_bidder_notifier',
                      text='BidPlaced -> HighestBidderNotifier', color='#000000'),
               Widget(id='connection_event_to_event_handler_outbid_notifier', text='BidderOutbid -> OutbidNotifier',
                      color='#000000'),
               Widget(id='connection_event_to_process_manager_auction', text='AuctionStarted -> AuctionProcessManager',
                      color='#000000'), Widget(id='connection_event_bid_placed_to_projection_auction_summary',
                                               text='BidPlaced -> AuctionSummary', color='#000000'),
               Widget(id='connection_event_bid_placed_to_projection_item_summary', text='BidPlaced -> ItemSummary',
                      color='#000000'), Widget(id='connection_event_bidder_outbid_to_projection_item_summary',
                                               text='BidderOutbid -> ItemSummary', color='#000000')]

    lines = [Line(id='connection_command_to_event_auction_started', start_widget_id='command_start_auction',
                  end_widget_id='event_auction_started', color='#000000'),
             Line(id='connection_command_to_event_bid_placed', start_widget_id='command_place_bid',
                  end_widget_id='event_bid_placed', color='#000000'),
             Line(id='connection_event_to_event_handler_highest_bidder_notifier', start_widget_id='event_bid_placed',
                  end_widget_id='event_handler_highest_bidder_notifier', color='#000000'),
             Line(id='connection_event_to_event_handler_outbid_notifier', start_widget_id='event_bidder_outbid',
                  end_widget_id='event_handler_outbid_notifier', color='#000000'),
             Line(id='connection_event_to_process_manager_auction_started', start_widget_id='event_auction_started',
                  end_widget_id='process_manager_auction', color='#000000'),
             Line(id='connection_event_to_process_manager_bid_placed', start_widget_id='event_bid_placed',
                  end_widget_id='process_manager_auction', color='#000000'),
             Line(id='connection_event_bid_placed_to_projection_auction_summary', start_widget_id='event_bid_placed',
                  end_widget_id='projection_auction_summary', color='#000000'),
             Line(id='connection_event_auction_started_to_projection_auction_summary',
                  start_widget_id='event_auction_started', end_widget_id='projection_auction_summary', color='#000000'),
             Line(id='connection_event_bid_placed_to_projection_item_summary', start_widget_id='event_bid_placed',
                  end_widget_id='projection_item_summary', color='#000000'),
             Line(id='connection_event_auction_started_to_projection_item_summary',
                  start_widget_id='event_auction_started', end_widget_id='projection_item_summary', color='#000000'),
             Line(id='connection_event_bidder_outbid_to_projection_item_summary', start_widget_id='event_bidder_outbid',
                  end_widget_id='projection_item_summary', color='#000000')]

    combined_response = {
        "type": "collection",
        "data": []
    }

    # response_widgets = ResponseWidgets(widgets=widgets)
    # response_lines = ResponseLines(lines=lines)

    response_widgets = ResponseWidgets(widgets=widgets)
    response_lines = ResponseLines(lines=lines)
    #
    # combined_response = create_combined_response(response_widgets, response_lines)
    # print(combined_response.json(indent=2))

    combined_response = []

    # Add widgets to the combined response
    for widget in response_widgets.widgets:
        combined_response.append({
            "id": widget.id,
            "type": "sticker",  # Assuming all are stickers, adjust as necessary
            "text": widget.text,
            "style": {
                "backgroundColor": widget.color
            }
        })

    # Add lines to the combined response
    for line in response_lines.lines:
        combined_response.append({
            "id": line.id,
            "type": "line",
            "startWidget": {
                "id": line.start_widget_id
            },
            "endWidget": {
                "id": line.end_widget_id
            },
            "style": {
                "strokeColor": line.color
            }
        })

    print(combined_response)


if __name__ == '__main__':
    main()
