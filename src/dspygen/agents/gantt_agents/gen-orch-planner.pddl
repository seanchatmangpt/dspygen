

(define (domain gen-orch-planner)
  (:requirements :strips)
  (:types
    var - object
    var_type - object
  )
  (:predicates
    
        
            (report_start_date ?r - var ?t - var)
        
            (report_end_date ?r - var ?t - var)
        
    
        
            (report_start_date ?r - var ?t - var)
        
            (report_end_date ?r - var ?t - var)
        
    
        
            (report_start_date ?r - var ?t - var)
        
            (report_end_date ?r - var ?t - var)
        
    
        
            (charge_date ?r - var ?t - var)
        
            (charge_amount ?r - var ?t - var)
        
    
        
            (help_topic ?r - var ?t - var)
        
    
        
            (contact_us_topic ?r - var ?t - var)
        
            (contact_us_channel ?r - var ?t - var)
        
    
        
            (invoice_amount ?r - var ?t - var)
        
            (invoice_detail ?r - var ?t - var)
        
    
        
            (customer_given_name ?r - var ?t - var)
        
            (customer_family_name ?r - var ?t - var)
        
            (customer_email ?r - var ?t - var)
        
            (customer_phone ?r - var ?t - var)
        
    
    (has_type ?a - var ?t - var_type)
    (has_value ?a - var)
  )
  
  
    
      
      (:action get_information_via_api
        :parameters (
          
            ?in_var - var
          
            ?in_type - var
          
          ?out - var
        )
        :precondition (and
          
            (has_type ?in_var string)
            (has_value ?in_var)
          
            (has_type ?in_type string)
            (has_value ?in_type)
          
          (has_type ?out get_information_via_api)
          (not (has_value ?out))
        )
        :effect (and
          
          (has_value ?out)
        )
      )
    
  
    
      
      (:action generate_profit_loss_report
        :parameters (
          
            ?start_date - var
          
            ?end_date - var
          
          ?out - var
        )
        :precondition (and
          
            (has_type ?start_date string)
            (has_value ?start_date)
          
            (has_type ?end_date string)
            (has_value ?end_date)
          
          (has_type ?out generate_profit_loss_report)
          (not (has_value ?out))
        )
        :effect (and
          
          (has_value ?out)
        )
      )
    
  
    
      
      (:action generate_expense_spend_report
        :parameters (
          
            ?start_date - var
          
            ?end_date - var
          
          ?out - var
        )
        :precondition (and
          
            (has_type ?start_date string)
            (has_value ?start_date)
          
            (has_type ?end_date string)
            (has_value ?end_date)
          
          (has_type ?out generate_expense_spend_report)
          (not (has_value ?out))
        )
        :effect (and
          
          (has_value ?out)
        )
      )
    
  
    
      
      (:action generate_invoice_sales_report
        :parameters (
          
            ?start_date - var
          
            ?end_date - var
          
          ?out - var
        )
        :precondition (and
          
            (has_type ?start_date string)
            (has_value ?start_date)
          
            (has_type ?end_date string)
            (has_value ?end_date)
          
          (has_type ?out generate_invoice_sales_report)
          (not (has_value ?out))
        )
        :effect (and
          
          (has_value ?out)
        )
      )
    
  
    
      
      (:action lookup_a_charge
        :parameters (
          
            ?charge_date - var
          
            ?amount - var
          
          ?out - var
        )
        :precondition (and
          
            (has_type ?charge_date string)
            (has_value ?charge_date)
          
            (has_type ?amount number)
            (has_value ?amount)
          
          (has_type ?out lookup_a_charge)
          (not (has_value ?out))
        )
        :effect (and
          
          (has_value ?out)
        )
      )
    
  
    
      
      (:action get_help_topic
        :parameters (
          
            ?topic - var
          
          ?out - var
        )
        :precondition (and
          
            (has_type ?topic string)
            (has_value ?topic)
          
          (has_type ?out get_help_topic)
          (not (has_value ?out))
        )
        :effect (and
          
          (has_value ?out)
        )
      )
    
  
    
      
      (:action contact_us_via_different_channels
        :parameters (
          
            ?topic - var
          
            ?channel - var
          
          ?out - var
        )
        :precondition (and
          
            (has_type ?topic string)
            (has_value ?topic)
          
            (has_type ?channel string)
            (has_value ?channel)
          
          (has_type ?out contact_us_via_different_channels)
          (not (has_value ?out))
        )
        :effect (and
          
          (has_value ?out)
        )
      )
    
  
    
      
      (:action create_a_new_invoice
        :parameters (
          
            ?amount - var
          
            ?detail - var
          
          ?out - var
        )
        :precondition (and
          
            (has_type ?amount number)
            (has_value ?amount)
          
            (has_type ?detail string)
            (has_value ?detail)
          
          (has_type ?out create_a_new_invoice)
          (not (has_value ?out))
        )
        :effect (and
          
          (has_value ?out)
        )
      )
    
  
    
      
      (:action update_customer_profile
        :parameters (
          
            ?given_name - var
          
            ?family_name - var
          
            ?email - var
          
            ?phone - var
          
          ?out - var
        )
        :precondition (and
          
            (has_type ?given_name string)
            (has_value ?given_name)
          
            (has_type ?family_name string)
            (has_value ?family_name)
          
            (has_type ?email string)
            (has_value ?email)
          
            (has_type ?phone string)
            (has_value ?phone)
          
          (has_type ?out update_customer_profile)
          (not (has_value ?out))
        )
        :effect (and
          
          (has_value ?out)
        )
      )
    
  
)