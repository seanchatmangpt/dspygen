from jinja2 import Template
import yaml



# Jinja2 template string (put the Jinja template content here)
template_str = """{% set predicates = {
    'profit_loss': ['report_start_date', 'report_end_date'],
    'expense_spend': ['report_start_date', 'report_end_date'],
    'invoice_sales': ['report_start_date', 'report_end_date'],
    'charge_lookup': ['charge_date', 'charge_amount'],
    'help': ['help_topic'],
    'contact_us': ['contact_us_topic', 'contact_us_channel'],
    'create_invoice': ['invoice_amount', 'invoice_detail'],
    'update_customer': ['customer_given_name', 'customer_family_name', 'customer_email', 'customer_phone']
} %}

(define (domain gen-orch-planner)
  (:requirements :strips)
  (:types
    var - object
    var_type - object
  )
  (:predicates
    {% for key, pred_list in predicates.items() %}
        {% for pred in pred_list %}
            ({{ pred }} ?r - var ?t - var)
        {% endfor %}
    {% endfor %}
    (has_type ?a - var ?t - var_type)
    (has_value ?a - var)
  )
  
  {% for path, methods in paths.items() %}
    {% for method, details in methods.items() %}
      {% set action_name = details.summary.lower().replace(' ', '_') %}
      (:action {{ action_name }}
        :parameters (
          {% for param_name, param in details.requestBody.content['application/json'].schema.properties.items() %}
            ?{{ param_name }} - var
          {% endfor %}
          ?out - var
        )
        :precondition (and
          {% for param_name, param in details.requestBody.content['application/json'].schema.properties.items() %}
            (has_type ?{{ param_name }} {{ param.type }})
            (has_value ?{{ param_name }})
          {% endfor %}
          (has_type ?out {{ action_name }})
          (not (has_value ?out))
        )
        :effect (and
          {% for pred in predicates[action_name] %}
            ({{ pred }} ?out ?{{ pred.split('_')[-1] }})
          {% endfor %}
          (has_value ?out)
        )
      )
    {% endfor %}
  {% endfor %}
)
"""


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()

    # Load your OpenAPI YAML file
    with open('openapi.yaml', 'r') as file:
        openapi_data = yaml.safe_load(file)

    # Create a Jinja2 Template object
    template = Template(template_str)

    # Render the template with the OpenAPI data
    pddl_output = template.render(paths=openapi_data['paths'])

    # Save the generated PDDL to a file
    with open('gen-orch-planner.pddl', 'w') as file:
        file.write(pddl_output)


if __name__ == '__main__':
    main()
