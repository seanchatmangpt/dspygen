
class EKEventStoreWrapper:
    def __init__(self):
        import EventKit
        self._ekeventstore = EventKit.EKEventStore.alloc().init()

    def cxx_destruct(self, *args, **kwargs):
        return self._ekeventstore.cxx_destruct(*args, **kwargs)

    def caml_type(self, *args, **kwargs):
        return self._ekeventstore.CAMLType(*args, **kwargs)

    def caml_type_for_key_(self, *args, **kwargs):
        return self._ekeventstore.CAMLTypeForKey_(*args, **kwargs)

    def caml_type_supported_for_key_(self, *args, **kwargs):
        return self._ekeventstore.CAMLTypeSupportedForKey_(*args, **kwargs)

    def c_a_add_value_multiplied_by_(self, *args, **kwargs):
        return self._ekeventstore.CA_addValue_multipliedBy_(*args, **kwargs)

    def c_a_archiving_value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.CA_archivingValueForKey_(*args, **kwargs)

    def c_a_copy_numeric_value_(self, *args, **kwargs):
        return self._ekeventstore.CA_copyNumericValue_(*args, **kwargs)

    def c_a_copy_render_value(self, *args, **kwargs):
        return self._ekeventstore.CA_copyRenderValue(*args, **kwargs)

    def c_a_copy_render_value_with_colorspace_(self, *args, **kwargs):
        return self._ekeventstore.CA_copyRenderValueWithColorspace_(*args, **kwargs)

    def c_a_distance_to_value_(self, *args, **kwargs):
        return self._ekeventstore.CA_distanceToValue_(*args, **kwargs)

    def c_a_interpolate_value_by_fraction_(self, *args, **kwargs):
        return self._ekeventstore.CA_interpolateValue_byFraction_(*args, **kwargs)

    def c_a_interpolate_values___interpolator_(self, *args, **kwargs):
        return self._ekeventstore.CA_interpolateValues___interpolator_(*args, **kwargs)

    def c_a_numeric_value_count(self, *args, **kwargs):
        return self._ekeventstore.CA_numericValueCount(*args, **kwargs)

    def c_a_prepare_render_value(self, *args, **kwargs):
        return self._ekeventstore.CA_prepareRenderValue(*args, **kwargs)

    def c_a_round_to_integer_from_value_(self, *args, **kwargs):
        return self._ekeventstore.CA_roundToIntegerFromValue_(*args, **kwargs)

    def c_a_validate_value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.CA_validateValue_forKey_(*args, **kwargs)

    def c_k_assign_to_container_with_id_(self, *args, **kwargs):
        return self._ekeventstore.CKAssignToContainerWithID_(*args, **kwargs)

    def c_k_description(self, *args, **kwargs):
        return self._ekeventstore.CKDescription(*args, **kwargs)

    def c_k_description_class_name(self, *args, **kwargs):
        return self._ekeventstore.CKDescriptionClassName(*args, **kwargs)

    def c_k_description_properties_with_public_private_should_expand_(self, *args, **kwargs):
        return self._ekeventstore.CKDescriptionPropertiesWithPublic_private_shouldExpand_(*args, **kwargs)

    def c_k_description_redact_avoid_short_description_(self, *args, **kwargs):
        return self._ekeventstore.CKDescriptionRedact_avoidShortDescription_(*args, **kwargs)

    def c_k_description_should_print_pointer(self, *args, **kwargs):
        return self._ekeventstore.CKDescriptionShouldPrintPointer(*args, **kwargs)

    def c_k_expanded_description(self, *args, **kwargs):
        return self._ekeventstore.CKExpandedDescription(*args, **kwargs)

    def c_k_object_description_redact_(self, *args, **kwargs):
        return self._ekeventstore.CKObjectDescriptionRedact_(*args, **kwargs)

    def c_k_object_description_redact_avoid_short_description_(self, *args, **kwargs):
        return self._ekeventstore.CKObjectDescriptionRedact_avoidShortDescription_(*args, **kwargs)

    def c_k_properties_description(self, *args, **kwargs):
        return self._ekeventstore.CKPropertiesDescription(*args, **kwargs)

    def c_k_redacted_description(self, *args, **kwargs):
        return self._ekeventstore.CKRedactedDescription(*args, **kwargs)

    def c_k_unredacted_description(self, *args, **kwargs):
        return self._ekeventstore.CKUnredactedDescription(*args, **kwargs)

    def cal_class_name(self, *args, **kwargs):
        return self._ekeventstore.CalClassName(*args, **kwargs)

    def i_c_s_data_for_calendar_items_options_(self, *args, **kwargs):
        return self._ekeventstore.ICSDataForCalendarItems_options_(*args, **kwargs)

    def i_c_s_data_for_calendar_items_prevent_line_folding_(self, *args, **kwargs):
        return self._ekeventstore.ICSDataForCalendarItems_preventLineFolding_(*args, **kwargs)

    def n_s_lifeguard_autorelease(self, *args, **kwargs):
        return self._ekeventstore.NSLifeguard_autorelease(*args, **kwargs)

    def n_s_representation(self, *args, **kwargs):
        return self._ekeventstore.NSRepresentation(*args, **kwargs)

    def n_s_observation_for_key_path_options_block_(self, *args, **kwargs):
        return self._ekeventstore.NS_observationForKeyPath_options_block_(*args, **kwargs)

    def n_s_observation_for_key_paths_options_block_(self, *args, **kwargs):
        return self._ekeventstore.NS_observationForKeyPaths_options_block_(*args, **kwargs)

    def r_b_s_is_x_p_c_object(self, *args, **kwargs):
        return self._ekeventstore.RBSIsXPCObject(*args, **kwargs)

    def s_c_n_u_i_name(self, *args, **kwargs):
        return self._ekeventstore.SCNUI_name(*args, **kwargs)

    def s_c_n_setup_display_link_with_queue_screen_policy_(self, *args, **kwargs):
        return self._ekeventstore.SCN_setupDisplayLinkWithQueue_screen_policy_(*args, **kwargs)

    def v_n_compute_device_performance_score(self, *args, **kwargs):
        return self._ekeventstore.VNComputeDevicePerformanceScore(*args, **kwargs)

    def v_n_compute_device_type(self, *args, **kwargs):
        return self._ekeventstore.VNComputeDeviceType(*args, **kwargs)

    def ab_case_insensitive_is_equal_(self, *args, **kwargs):
        return self._ekeventstore.abCaseInsensitiveIsEqual_(*args, **kwargs)

    def ab_dictionary_with_values_for_key_paths_(self, *args, **kwargs):
        return self._ekeventstore.abDictionaryWithValuesForKeyPaths_(*args, **kwargs)

    def ab_remove_observer_ignoring_exceptions_for_key_path_(self, *args, **kwargs):
        return self._ekeventstore.abRemoveObserverIgnoringExceptions_forKeyPath_(*args, **kwargs)

    def accept_suggested_event_(self, *args, **kwargs):
        return self._ekeventstore.acceptSuggestedEvent_(*args, **kwargs)

    def accept_suggested_event_place_on_calendar_(self, *args, **kwargs):
        return self._ekeventstore.acceptSuggestedEvent_placeOnCalendar_(*args, **kwargs)

    def access_granted_for_entity_type_(self, *args, **kwargs):
        return self._ekeventstore.accessGrantedForEntityType_(*args, **kwargs)

    def accessibility_add_temporary_child_(self, *args, **kwargs):
        return self._ekeventstore.accessibilityAddTemporaryChild_(*args, **kwargs)

    def accessibility_allows_overridden_attributes_when_ignored(self, *args, **kwargs):
        return self._ekeventstore.accessibilityAllowsOverriddenAttributesWhenIgnored(*args, **kwargs)

    def accessibility_array_attribute_count_(self, *args, **kwargs):
        return self._ekeventstore.accessibilityArrayAttributeCount_(*args, **kwargs)

    def accessibility_array_attribute_values_index_max_count_(self, *args, **kwargs):
        return self._ekeventstore.accessibilityArrayAttributeValues_index_maxCount_(*args, **kwargs)

    def accessibility_attribute_value_for_parameter_(self, *args, **kwargs):
        return self._ekeventstore.accessibilityAttributeValue_forParameter_(*args, **kwargs)

    def accessibility_attributed_value_for_string_attribute_attribute_for_parameter_(self, *args, **kwargs):
        return self._ekeventstore.accessibilityAttributedValueForStringAttributeAttributeForParameter_(*args, **kwargs)

    def accessibility_braille_map_render_region(self, *args, **kwargs):
        return self._ekeventstore.accessibilityBrailleMapRenderRegion(*args, **kwargs)

    def accessibility_braille_map_renderer(self, *args, **kwargs):
        return self._ekeventstore.accessibilityBrailleMapRenderer(*args, **kwargs)

    def accessibility_decode_overridden_attributes_(self, *args, **kwargs):
        return self._ekeventstore.accessibilityDecodeOverriddenAttributes_(*args, **kwargs)

    def accessibility_encode_overridden_attributes_(self, *args, **kwargs):
        return self._ekeventstore.accessibilityEncodeOverriddenAttributes_(*args, **kwargs)

    def accessibility_index_for_child_u_i_element_attribute_for_parameter_(self, *args, **kwargs):
        return self._ekeventstore.accessibilityIndexForChildUIElementAttributeForParameter_(*args, **kwargs)

    def accessibility_index_of_child_(self, *args, **kwargs):
        return self._ekeventstore.accessibilityIndexOfChild_(*args, **kwargs)

    def accessibility_overridden_attributes(self, *args, **kwargs):
        return self._ekeventstore.accessibilityOverriddenAttributes(*args, **kwargs)

    def accessibility_parameterized_attribute_names(self, *args, **kwargs):
        return self._ekeventstore.accessibilityParameterizedAttributeNames(*args, **kwargs)

    def accessibility_perform_show_menu_of_child_(self, *args, **kwargs):
        return self._ekeventstore.accessibilityPerformShowMenuOfChild_(*args, **kwargs)

    def accessibility_presenter_process_identifier(self, *args, **kwargs):
        return self._ekeventstore.accessibilityPresenterProcessIdentifier(*args, **kwargs)

    def accessibility_remove_temporary_child_(self, *args, **kwargs):
        return self._ekeventstore.accessibilityRemoveTemporaryChild_(*args, **kwargs)

    def accessibility_replace_range_with_text_(self, *args, **kwargs):
        return self._ekeventstore.accessibilityReplaceRange_withText_(*args, **kwargs)

    def accessibility_set_override_value_for_attribute_(self, *args, **kwargs):
        return self._ekeventstore.accessibilitySetOverrideValue_forAttribute_(*args, **kwargs)

    def accessibility_set_presenter_process_identifier_(self, *args, **kwargs):
        return self._ekeventstore.accessibilitySetPresenterProcessIdentifier_(*args, **kwargs)

    def accessibility_should_send_notification_(self, *args, **kwargs):
        return self._ekeventstore.accessibilityShouldSendNotification_(*args, **kwargs)

    def accessibility_should_use_unique_id(self, *args, **kwargs):
        return self._ekeventstore.accessibilityShouldUseUniqueId(*args, **kwargs)

    def accessibility_supports_custom_element_data(self, *args, **kwargs):
        return self._ekeventstore.accessibilitySupportsCustomElementData(*args, **kwargs)

    def accessibility_supports_notifications(self, *args, **kwargs):
        return self._ekeventstore.accessibilitySupportsNotifications(*args, **kwargs)

    def accessibility_supports_overridden_attributes(self, *args, **kwargs):
        return self._ekeventstore.accessibilitySupportsOverriddenAttributes(*args, **kwargs)

    def accessibility_temporary_children(self, *args, **kwargs):
        return self._ekeventstore.accessibilityTemporaryChildren(*args, **kwargs)

    def accessibility_visible_area(self, *args, **kwargs):
        return self._ekeventstore.accessibilityVisibleArea(*args, **kwargs)

    def acknowledge_notifications_error_(self, *args, **kwargs):
        return self._ekeventstore.acknowledgeNotifications_error_(*args, **kwargs)

    def acquire_default_calendar_for_new_events(self, *args, **kwargs):
        return self._ekeventstore.acquireDefaultCalendarForNewEvents(*args, **kwargs)

    def acquire_default_calendar_for_new_reminders(self, *args, **kwargs):
        return self._ekeventstore.acquireDefaultCalendarForNewReminders(*args, **kwargs)

    def add_chained_observers_(self, *args, **kwargs):
        return self._ekeventstore.addChainedObservers_(*args, **kwargs)

    def add_exchange_delegate_with_name_email_address_to_source_completion_(self, *args, **kwargs):
        return self._ekeventstore.addExchangeDelegateWithName_emailAddress_toSource_completion_(*args, **kwargs)

    def add_object_to_both_sides_of_relationship_with_key_(self, *args, **kwargs):
        return self._ekeventstore.addObject_toBothSidesOfRelationshipWithKey_(*args, **kwargs)

    def add_object_to_property_with_key_(self, *args, **kwargs):
        return self._ekeventstore.addObject_toPropertyWithKey_(*args, **kwargs)

    def add_observation_transformer_(self, *args, **kwargs):
        return self._ekeventstore.addObservationTransformer_(*args, **kwargs)

    def add_observer_block_(self, *args, **kwargs):
        return self._ekeventstore.addObserverBlock_(*args, **kwargs)

    def add_observer_(self, *args, **kwargs):
        return self._ekeventstore.addObserver_(*args, **kwargs)

    def add_observer_for_key_path_options_context_(self, *args, **kwargs):
        return self._ekeventstore.addObserver_forKeyPath_options_context_(*args, **kwargs)

    def add_observer_for_observable_key_path_(self, *args, **kwargs):
        return self._ekeventstore.addObserver_forObservableKeyPath_(*args, **kwargs)

    def address_validation_status_(self, *args, **kwargs):
        return self._ekeventstore.addressValidationStatus_(*args, **kwargs)

    def alarm_occurrences_between_start_date_end_date_in_calendars_completion_(self, *args, **kwargs):
        return self._ekeventstore.alarmOccurrencesBetweenStartDate_endDate_inCalendars_completion_(*args, **kwargs)

    def alarm_with_external_id_(self, *args, **kwargs):
        return self._ekeventstore.alarmWithExternalID_(*args, **kwargs)

    def alarm_with_u_u_id_(self, *args, **kwargs):
        return self._ekeventstore.alarmWithUUID_(*args, **kwargs)

    def all_events_with_unique_id_occurrence_date_(self, *args, **kwargs):
        return self._ekeventstore.allEventsWithUniqueId_occurrenceDate_(*args, **kwargs)

    def all_property_keys(self, *args, **kwargs):
        return self._ekeventstore.allPropertyKeys(*args, **kwargs)

    def allow_access_to_events_only(self, *args, **kwargs):
        return self._ekeventstore.allowAccessToEventsOnly(*args, **kwargs)

    def allow_delegate_sources(self, *args, **kwargs):
        return self._ekeventstore.allowDelegateSources(*args, **kwargs)

    def allows_birthday_modifications(self, *args, **kwargs):
        return self._ekeventstore.allowsBirthdayModifications(*args, **kwargs)

    def allows_weak_reference(self, *args, **kwargs):
        return self._ekeventstore.allowsWeakReference(*args, **kwargs)

    def analytics_send_event_appending_client_bundle_id_to_payload_(self, *args, **kwargs):
        return self._ekeventstore.analyticsSendEvent_appendingClientBundleIDToPayload_(*args, **kwargs)

    def attachment_with_u_u_id_(self, *args, **kwargs):
        return self._ekeventstore.attachmentWithUUID_(*args, **kwargs)

    def attribute_keys(self, *args, **kwargs):
        return self._ekeventstore.attributeKeys(*args, **kwargs)

    def auto_content_accessing_proxy(self, *args, **kwargs):
        return self._ekeventstore.autoContentAccessingProxy(*args, **kwargs)

    def automatic_location_geocoding_allowed(self, *args, **kwargs):
        return self._ekeventstore.automaticLocationGeocodingAllowed(*args, **kwargs)

    def autorelease(self, *args, **kwargs):
        return self._ekeventstore.autorelease(*args, **kwargs)

    def awake_after_using_coder_(self, *args, **kwargs):
        return self._ekeventstore.awakeAfterUsingCoder_(*args, **kwargs)

    def awake_from_nib(self, *args, **kwargs):
        return self._ekeventstore.awakeFromNib(*args, **kwargs)

    def backup_database_to_destination_with_format_error_(self, *args, **kwargs):
        return self._ekeventstore.backupDatabaseToDestination_withFormat_error_(*args, **kwargs)

    def begin_cal_d_a_v_server_simulation_with_hostname_(self, *args, **kwargs):
        return self._ekeventstore.beginCalDAVServerSimulationWithHostname_(*args, **kwargs)

    def bind_to_object_with_key_path_options_(self, *args, **kwargs):
        return self._ekeventstore.bind_toObject_withKeyPath_options_(*args, **kwargs)

    def birthday_calendar_enabled(self, *args, **kwargs):
        return self._ekeventstore.birthdayCalendarEnabled(*args, **kwargs)

    def birthday_calendar_version(self, *args, **kwargs):
        return self._ekeventstore.birthdayCalendarVersion(*args, **kwargs)

    def bool_value_safe(self, *args, **kwargs):
        return self._ekeventstore.boolValueSafe(*args, **kwargs)

    def bool_value_safe_(self, *args, **kwargs):
        return self._ekeventstore.boolValueSafe_(*args, **kwargs)

    def bs_is_plistable_type(self, *args, **kwargs):
        return self._ekeventstore.bs_isPlistableType(*args, **kwargs)

    def bs_secure_encoded(self, *args, **kwargs):
        return self._ekeventstore.bs_secureEncoded(*args, **kwargs)

    def cache_constraints_for_object_with_c_a_d_object_id_(self, *args, **kwargs):
        return self._ekeventstore.cacheConstraints_forObjectWithCADObjectID_(*args, **kwargs)

    def cache_validation_status_for_address_status_(self, *args, **kwargs):
        return self._ekeventstore.cacheValidationStatusForAddress_status_(*args, **kwargs)

    def cached_constraints_for_calendar_(self, *args, **kwargs):
        return self._ekeventstore.cachedConstraintsForCalendar_(*args, **kwargs)

    def cached_constraints_for_event_or_source_with_c_a_d_object_id_(self, *args, **kwargs):
        return self._ekeventstore.cachedConstraintsForEventOrSourceWithCADObjectID_(*args, **kwargs)

    def cached_constraints_for_event_(self, *args, **kwargs):
        return self._ekeventstore.cachedConstraintsForEvent_(*args, **kwargs)

    def cached_constraints_for_reminder_(self, *args, **kwargs):
        return self._ekeventstore.cachedConstraintsForReminder_(*args, **kwargs)

    def cached_constraints_for_source_(self, *args, **kwargs):
        return self._ekeventstore.cachedConstraintsForSource_(*args, **kwargs)

    def calendar_item_with_identifier_(self, *args, **kwargs):
        return self._ekeventstore.calendarItemWithIdentifier_(*args, **kwargs)

    def calendar_items_with_external_identifier_(self, *args, **kwargs):
        return self._ekeventstore.calendarItemsWithExternalIdentifier_(*args, **kwargs)

    def calendar_items_with_external_identifier_in_calendars_(self, *args, **kwargs):
        return self._ekeventstore.calendarItemsWithExternalIdentifier_inCalendars_(*args, **kwargs)

    def calendar_items_with_unique_identifier_in_calendar_(self, *args, **kwargs):
        return self._ekeventstore.calendarItemsWithUniqueIdentifier_inCalendar_(*args, **kwargs)

    def calendar_sources_and_defaults_queue(self, *args, **kwargs):
        return self._ekeventstore.calendarSourcesAndDefaultsQueue(*args, **kwargs)

    def calendar_with_c_a_d_id_(self, *args, **kwargs):
        return self._ekeventstore.calendarWithCADID_(*args, **kwargs)

    def calendar_with_external_id_(self, *args, **kwargs):
        return self._ekeventstore.calendarWithExternalID_(*args, **kwargs)

    def calendar_with_external_u_r_i_(self, *args, **kwargs):
        return self._ekeventstore.calendarWithExternalURI_(*args, **kwargs)

    def calendar_with_id_(self, *args, **kwargs):
        return self._ekeventstore.calendarWithID_(*args, **kwargs)

    def calendar_with_identifier_(self, *args, **kwargs):
        return self._ekeventstore.calendarWithIdentifier_(*args, **kwargs)

    def calendar_with_unique_id_(self, *args, **kwargs):
        return self._ekeventstore.calendarWithUniqueID_(*args, **kwargs)

    def calendars(self, *args, **kwargs):
        return self._ekeventstore.calendars(*args, **kwargs)

    def calendars_for_entity_type_(self, *args, **kwargs):
        return self._ekeventstore.calendarsForEntityType_(*args, **kwargs)

    def calendars_for_entity_type_in_source_(self, *args, **kwargs):
        return self._ekeventstore.calendarsForEntityType_inSource_(*args, **kwargs)

    def calendars_with_identifiers_(self, *args, **kwargs):
        return self._ekeventstore.calendarsWithIdentifiers_(*args, **kwargs)

    def calendars_with_object_ids_(self, *args, **kwargs):
        return self._ekeventstore.calendarsWithObjectIDs_(*args, **kwargs)

    def can_modify_calendar_database(self, *args, **kwargs):
        return self._ekeventstore.canModifyCalendarDatabase(*args, **kwargs)

    def can_modify_suggested_event_calendar(self, *args, **kwargs):
        return self._ekeventstore.canModifySuggestedEventCalendar(*args, **kwargs)

    def cancel_fetch_request_(self, *args, **kwargs):
        return self._ekeventstore.cancelFetchRequest_(*args, **kwargs)

    def changed_object_ids_since_token_result_handler_(self, *args, **kwargs):
        return self._ekeventstore.changedObjectIDsSinceToken_resultHandler_(*args, **kwargs)

    def changes_since_sequence_token_completion_(self, *args, **kwargs):
        return self._ekeventstore.changesSinceSequenceToken_completion_(*args, **kwargs)

    def ck_bind_in_statement_at_index_(self, *args, **kwargs):
        return self._ekeventstore.ck_bindInStatement_atIndex_(*args, **kwargs)

    def cksqlcs_append_s_q_l_constant_value_to_string_(self, *args, **kwargs):
        return self._ekeventstore.cksqlcs_appendSQLConstantValueToString_(*args, **kwargs)

    def cksqlcs_archived_object_binding_value_(self, *args, **kwargs):
        return self._ekeventstore.cksqlcs_archivedObjectBindingValue_(*args, **kwargs)

    def cksqlcs_bind_archived_object_index_db_(self, *args, **kwargs):
        return self._ekeventstore.cksqlcs_bindArchivedObject_index_db_(*args, **kwargs)

    def cksqlcs_bind_blob_index_db_(self, *args, **kwargs):
        return self._ekeventstore.cksqlcs_bindBlob_index_db_(*args, **kwargs)

    def cksqlcs_bind_double_index_db_(self, *args, **kwargs):
        return self._ekeventstore.cksqlcs_bindDouble_index_db_(*args, **kwargs)

    def cksqlcs_bind_int64_index_db_(self, *args, **kwargs):
        return self._ekeventstore.cksqlcs_bindInt64_index_db_(*args, **kwargs)

    def cksqlcs_bind_text_index_db_(self, *args, **kwargs):
        return self._ekeventstore.cksqlcs_bindText_index_db_(*args, **kwargs)

    def cksqlcs_blob_binding_value_destructor_error_(self, *args, **kwargs):
        return self._ekeventstore.cksqlcs_blobBindingValue_destructor_error_(*args, **kwargs)

    def cksqlcs_double_binding_value_(self, *args, **kwargs):
        return self._ekeventstore.cksqlcs_doubleBindingValue_(*args, **kwargs)

    def cksqlcs_int64_binding_value_(self, *args, **kwargs):
        return self._ekeventstore.cksqlcs_int64BindingValue_(*args, **kwargs)

    def cksqlcs_text_binding_value_destructor_error_(self, *args, **kwargs):
        return self._ekeventstore.cksqlcs_textBindingValue_destructor_error_(*args, **kwargs)

    def class_code(self, *args, **kwargs):
        return self._ekeventstore.classCode(*args, **kwargs)

    def class_description(self, *args, **kwargs):
        return self._ekeventstore.classDescription(*args, **kwargs)

    def class_description_for_destination_key_(self, *args, **kwargs):
        return self._ekeventstore.classDescriptionForDestinationKey_(*args, **kwargs)

    def class_for_archiver(self, *args, **kwargs):
        return self._ekeventstore.classForArchiver(*args, **kwargs)

    def class_for_coder(self, *args, **kwargs):
        return self._ekeventstore.classForCoder(*args, **kwargs)

    def class_for_keyed_archiver(self, *args, **kwargs):
        return self._ekeventstore.classForKeyedArchiver(*args, **kwargs)

    def class_for_port_coder(self, *args, **kwargs):
        return self._ekeventstore.classForPortCoder(*args, **kwargs)

    def class_name(self, *args, **kwargs):
        return self._ekeventstore.className(*args, **kwargs)

    def class__(self, *args, **kwargs):
        return self._ekeventstore.class__(*args, **kwargs)

    def clear_properties(self, *args, **kwargs):
        return self._ekeventstore.clearProperties(*args, **kwargs)

    def clear_superfluous_changes(self, *args, **kwargs):
        return self._ekeventstore.clearSuperfluousChanges(*args, **kwargs)

    def client_can_modify_sources(self, *args, **kwargs):
        return self._ekeventstore.clientCanModifySources(*args, **kwargs)

    def closest_cached_occurrence_to_date_for_event_object_id_(self, *args, **kwargs):
        return self._ekeventstore.closestCachedOccurrenceToDate_forEventObjectID_(*args, **kwargs)

    def closest_cached_occurrence_to_date_for_event_object_id_prefers_forward_search_(self, *args, **kwargs):
        return self._ekeventstore.closestCachedOccurrenceToDate_forEventObjectID_prefersForwardSearch_(*args, **kwargs)

    def coerce_value_for_scripting_properties_(self, *args, **kwargs):
        return self._ekeventstore.coerceValueForScriptingProperties_(*args, **kwargs)

    def coerce_value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.coerceValue_forKey_(*args, **kwargs)

    def color_string_for_new_calendar(self, *args, **kwargs):
        return self._ekeventstore.colorStringForNewCalendar(*args, **kwargs)

    def combine_event_calendars_with_reminder_calendars_(self, *args, **kwargs):
        return self._ekeventstore.combineEventCalendars_withReminderCalendars_(*args, **kwargs)

    def combined_reminder_and_event_sources(self, *args, **kwargs):
        return self._ekeventstore.combinedReminderAndEventSources(*args, **kwargs)

    def commit_objects_error_(self, *args, **kwargs):
        return self._ekeventstore.commitObjects_error_(*args, **kwargs)

    def commit_with_rollback_for_new_clients_(self, *args, **kwargs):
        return self._ekeventstore.commitWithRollbackForNewClients_(*args, **kwargs)

    def commit_with_rollback_(self, *args, **kwargs):
        return self._ekeventstore.commitWithRollback_(*args, **kwargs)

    def commit_(self, *args, **kwargs):
        return self._ekeventstore.commit_(*args, **kwargs)

    def confirm_suggested_event_(self, *args, **kwargs):
        return self._ekeventstore.confirmSuggestedEvent_(*args, **kwargs)

    def conforms_to_protocol_(self, *args, **kwargs):
        return self._ekeventstore.conformsToProtocol_(*args, **kwargs)

    def connection(self, *args, **kwargs):
        return self._ekeventstore.connection(*args, **kwargs)

    def constraints_cache_queue(self, *args, **kwargs):
        return self._ekeventstore.constraintsCacheQueue(*args, **kwargs)

    def consume_all_changes_up_to_token_(self, *args, **kwargs):
        return self._ekeventstore.consumeAllChangesUpToToken_(*args, **kwargs)

    def consume_all_changes_up_to_token_except_error_(self, *args, **kwargs):
        return self._ekeventstore.consumeAllChangesUpToToken_except_error_(*args, **kwargs)

    def copy(self, *args, **kwargs):
        return self._ekeventstore.copy(*args, **kwargs)

    def copy_c_g_color_for_new_calendar(self, *args, **kwargs):
        return self._ekeventstore.copyCGColorForNewCalendar(*args, **kwargs)

    def copy_scripting_value_for_key_with_properties_(self, *args, **kwargs):
        return self._ekeventstore.copyScriptingValue_forKey_withProperties_(*args, **kwargs)

    def count_of_events_from_start_date_to_end_date_(self, *args, **kwargs):
        return self._ekeventstore.countOfEventsFromStartDate_toEndDate_(*args, **kwargs)

    def create_key_value_binding_for_key_type_mask_(self, *args, **kwargs):
        return self._ekeventstore.createKeyValueBindingForKey_typeMask_(*args, **kwargs)

    def creator_team_identifier_for_event_(self, *args, **kwargs):
        return self._ekeventstore.creatorTeamIdentifierForEvent_(*args, **kwargs)

    def daemon_restarted(self, *args, **kwargs):
        return self._ekeventstore.daemonRestarted(*args, **kwargs)

    def data_protection_observer(self, *args, **kwargs):
        return self._ekeventstore.dataProtectionObserver(*args, **kwargs)

    def database(self, *args, **kwargs):
        return self._ekeventstore.database(*args, **kwargs)

    def database_path(self, *args, **kwargs):
        return self._ekeventstore.databasePath(*args, **kwargs)

    def database_restore_generation_changed_externally_(self, *args, **kwargs):
        return self._ekeventstore.databaseRestoreGenerationChangedExternally_(*args, **kwargs)

    def db_changed_queue(self, *args, **kwargs):
        return self._ekeventstore.dbChangedQueue(*args, **kwargs)

    def db_stats_by_source(self, *args, **kwargs):
        return self._ekeventstore.dbStatsBySource(*args, **kwargs)

    def dealloc(self, *args, **kwargs):
        return self._ekeventstore.dealloc(*args, **kwargs)

    def debug_description(self, *args, **kwargs):
        return self._ekeventstore.debugDescription(*args, **kwargs)

    def default_all_day_alarm(self, *args, **kwargs):
        return self._ekeventstore.defaultAllDayAlarm(*args, **kwargs)

    def default_all_day_alarm_offset(self, *args, **kwargs):
        return self._ekeventstore.defaultAllDayAlarmOffset(*args, **kwargs)

    def default_calendar_for_new_events(self, *args, **kwargs):
        return self._ekeventstore.defaultCalendarForNewEvents(*args, **kwargs)

    def default_calendar_for_new_events_in_delegate_source_(self, *args, **kwargs):
        return self._ekeventstore.defaultCalendarForNewEventsInDelegateSource_(*args, **kwargs)

    def default_calendar_for_new_reminders(self, *args, **kwargs):
        return self._ekeventstore.defaultCalendarForNewReminders(*args, **kwargs)

    def default_local_calendar(self, *args, **kwargs):
        return self._ekeventstore.defaultLocalCalendar(*args, **kwargs)

    def default_timed_alarm(self, *args, **kwargs):
        return self._ekeventstore.defaultTimedAlarm(*args, **kwargs)

    def default_timed_alarm_offset(self, *args, **kwargs):
        return self._ekeventstore.defaultTimedAlarmOffset(*args, **kwargs)

    def delegate_sources(self, *args, **kwargs):
        return self._ekeventstore.delegateSources(*args, **kwargs)

    def delegate_sources_for_source_(self, *args, **kwargs):
        return self._ekeventstore.delegateSourcesForSource_(*args, **kwargs)

    def delete_calendar_for_entity_type_error_(self, *args, **kwargs):
        return self._ekeventstore.deleteCalendar_forEntityType_error_(*args, **kwargs)

    def delete_draft_of_event_with_occurrence_id_(self, *args, **kwargs):
        return self._ekeventstore.deleteDraftOfEventWithOccurrenceID_(*args, **kwargs)

    def delete_suggested_event_(self, *args, **kwargs):
        return self._ekeventstore.deleteSuggestedEvent_(*args, **kwargs)

    def deleted_object_ids(self, *args, **kwargs):
        return self._ekeventstore.deletedObjectIDs(*args, **kwargs)

    def deleted_object_ids_pending_commit(self, *args, **kwargs):
        return self._ekeventstore.deletedObjectIDsPendingCommit(*args, **kwargs)

    def deleted_objects(self, *args, **kwargs):
        return self._ekeventstore.deletedObjects(*args, **kwargs)

    def description(self, *args, **kwargs):
        return self._ekeventstore.description(*args, **kwargs)

    def description_at_indent_(self, *args, **kwargs):
        return self._ekeventstore.descriptionAtIndent_(*args, **kwargs)

    def dictionary_with_values_for_keys_(self, *args, **kwargs):
        return self._ekeventstore.dictionaryWithValuesForKeys_(*args, **kwargs)

    def did_change_value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.didChangeValueForKey_(*args, **kwargs)

    def did_change_value_for_key_with_set_mutation_using_objects_(self, *args, **kwargs):
        return self._ekeventstore.didChangeValueForKey_withSetMutation_usingObjects_(*args, **kwargs)

    def did_change_values_at_indexes_for_key_(self, *args, **kwargs):
        return self._ekeventstore.didChange_valuesAtIndexes_forKey_(*args, **kwargs)

    def do_events_have_occurrences_after_date_(self, *args, **kwargs):
        return self._ekeventstore.doEvents_haveOccurrencesAfterDate_(*args, **kwargs)

    def does_contain_(self, *args, **kwargs):
        return self._ekeventstore.doesContain_(*args, **kwargs)

    def does_not_recognize_selector_(self, *args, **kwargs):
        return self._ekeventstore.doesNotRecognizeSelector_(*args, **kwargs)

    def double_value_safe(self, *args, **kwargs):
        return self._ekeventstore.doubleValueSafe(*args, **kwargs)

    def double_value_safe_(self, *args, **kwargs):
        return self._ekeventstore.doubleValueSafe_(*args, **kwargs)

    def enable_source_sync_status_changes(self, *args, **kwargs):
        return self._ekeventstore.enableSourceSyncStatusChanges(*args, **kwargs)

    def encode_with_caml_writer_(self, *args, **kwargs):
        return self._ekeventstore.encodeWithCAMLWriter_(*args, **kwargs)

    def end_cal_d_a_v_server_simulation_(self, *args, **kwargs):
        return self._ekeventstore.endCalDAVServerSimulation_(*args, **kwargs)

    def ensure_loaded_properties_for_objects_(self, *args, **kwargs):
        return self._ekeventstore.ensureLoadedProperties_forObjects_(*args, **kwargs)

    def entity_name(self, *args, **kwargs):
        return self._ekeventstore.entityName(*args, **kwargs)

    def enumerate_events_matching_predicate_using_block_(self, *args, **kwargs):
        return self._ekeventstore.enumerateEventsMatchingPredicate_usingBlock_(*args, **kwargs)

    def event_access_level(self, *args, **kwargs):
        return self._ekeventstore.eventAccessLevel(*args, **kwargs)

    def event_for_object_id_occurrence_date_(self, *args, **kwargs):
        return self._ekeventstore.eventForObjectID_occurrenceDate_(*args, **kwargs)

    def event_for_object_id_occurrence_date_check_valid_(self, *args, **kwargs):
        return self._ekeventstore.eventForObjectID_occurrenceDate_checkValid_(*args, **kwargs)

    def event_for_u_id_occurrence_date_(self, *args, **kwargs):
        return self._ekeventstore.eventForUID_occurrenceDate_(*args, **kwargs)

    def event_for_u_id_occurrence_date_check_valid_(self, *args, **kwargs):
        return self._ekeventstore.eventForUID_occurrenceDate_checkValid_(*args, **kwargs)

    def event_notification_count(self, *args, **kwargs):
        return self._ekeventstore.eventNotificationCount(*args, **kwargs)

    def event_notification_count_excluding_unchecked_calendars_expanded_(self, *args, **kwargs):
        return self._ekeventstore.eventNotificationCountExcludingUncheckedCalendars_expanded_(*args, **kwargs)

    def event_notification_count_expanded_(self, *args, **kwargs):
        return self._ekeventstore.eventNotificationCountExpanded_(*args, **kwargs)

    def event_notification_count_for_source_excluding_delegate_sources_filtered_by_shows_notifications_flag_exclude_object_ids_(self, *args, **kwargs):
        return self._ekeventstore.eventNotificationCountForSource_excludingDelegateSources_filteredByShowsNotificationsFlag_excludeObjectIDs_(*args, **kwargs)

    def event_notification_count_for_source_excluding_delegate_sources_filtered_by_shows_notifications_flag_exclude_object_ids_expanded_(self, *args, **kwargs):
        return self._ekeventstore.eventNotificationCountForSource_excludingDelegateSources_filteredByShowsNotificationsFlag_excludeObjectIDs_expanded_(*args, **kwargs)

    def event_notifications(self, *args, **kwargs):
        return self._ekeventstore.eventNotifications(*args, **kwargs)

    def event_notifications_after_date_(self, *args, **kwargs):
        return self._ekeventstore.eventNotificationsAfterDate_(*args, **kwargs)

    def event_notifications_after_date_excluding_unchecked_calendars_filtered_by_shows_notifications_flag_earliest_expiring_notification_(self, *args, **kwargs):
        return self._ekeventstore.eventNotificationsAfterDate_excludingUncheckedCalendars_filteredByShowsNotificationsFlag_earliestExpiringNotification_(*args, **kwargs)

    def event_notifications_after_date_filtered_by_shows_notifications_flag_earliest_expiring_notification_(self, *args, **kwargs):
        return self._ekeventstore.eventNotificationsAfterDate_filteredByShowsNotificationsFlag_earliestExpiringNotification_(*args, **kwargs)

    def event_notifications_excluding_unchecked_calendars_filtered_by_shows_notifications_flag_earliest_expiring_notification_(self, *args, **kwargs):
        return self._ekeventstore.eventNotificationsExcludingUncheckedCalendars_filteredByShowsNotificationsFlag_earliestExpiringNotification_(*args, **kwargs)

    def event_object_ids_matching_predicate_(self, *args, **kwargs):
        return self._ekeventstore.eventObjectIDsMatchingPredicate_(*args, **kwargs)

    def event_source_for_reminder_source_(self, *args, **kwargs):
        return self._ekeventstore.eventSourceForReminderSource_(*args, **kwargs)

    def event_source_id_for_reminder_source_id_(self, *args, **kwargs):
        return self._ekeventstore.eventSourceIDForReminderSourceID_(*args, **kwargs)

    def event_source_id_to_reminder_source_id_mapping(self, *args, **kwargs):
        return self._ekeventstore.eventSourceIDToReminderSourceIDMapping(*args, **kwargs)

    def event_source_map(self, *args, **kwargs):
        return self._ekeventstore.eventSourceMap(*args, **kwargs)

    def event_sources(self, *args, **kwargs):
        return self._ekeventstore.eventSources(*args, **kwargs)

    def event_store_identifier(self, *args, **kwargs):
        return self._ekeventstore.eventStoreIdentifier(*args, **kwargs)

    def event_with_external_u_r_i_(self, *args, **kwargs):
        return self._ekeventstore.eventWithExternalURI_(*args, **kwargs)

    def event_with_identifier_(self, *args, **kwargs):
        return self._ekeventstore.eventWithIdentifier_(*args, **kwargs)

    def event_with_recurrence_identifier_(self, *args, **kwargs):
        return self._ekeventstore.eventWithRecurrenceIdentifier_(*args, **kwargs)

    def event_with_u_u_id_(self, *args, **kwargs):
        return self._ekeventstore.eventWithUUID_(*args, **kwargs)

    def event_with_u_u_id_is_in_calendars_(self, *args, **kwargs):
        return self._ekeventstore.eventWithUUID_isInCalendars_(*args, **kwargs)

    def event_with_u_u_id_occurrence_date_(self, *args, **kwargs):
        return self._ekeventstore.eventWithUUID_occurrenceDate_(*args, **kwargs)

    def event_with_unique_id_(self, *args, **kwargs):
        return self._ekeventstore.eventWithUniqueId_(*args, **kwargs)

    def event_with_unique_id_occurrence_date_(self, *args, **kwargs):
        return self._ekeventstore.eventWithUniqueId_occurrenceDate_(*args, **kwargs)

    def event_with_unique_identifier_(self, *args, **kwargs):
        return self._ekeventstore.eventWithUniqueIdentifier_(*args, **kwargs)

    def events_exist_on_calendar_(self, *args, **kwargs):
        return self._ekeventstore.eventsExistOnCalendar_(*args, **kwargs)

    def events_marked_schedule_agent_client_exist_on_calendar_(self, *args, **kwargs):
        return self._ekeventstore.eventsMarkedScheduleAgentClientExistOnCalendar_(*args, **kwargs)

    def events_matching_predicate_(self, *args, **kwargs):
        return self._ekeventstore.eventsMatchingPredicate_(*args, **kwargs)

    def events_with_errors_per_source_id(self, *args, **kwargs):
        return self._ekeventstore.eventsWithErrorsPerSourceID(*args, **kwargs)

    def events_with_external_identifier_in_calendars_(self, *args, **kwargs):
        return self._ekeventstore.eventsWithExternalIdentifier_inCalendars_(*args, **kwargs)

    def events_with_identifiers_(self, *args, **kwargs):
        return self._ekeventstore.eventsWithIdentifiers_(*args, **kwargs)

    def events_with_u_u_id_to_occurrence_date_map_in_calendars_(self, *args, **kwargs):
        return self._ekeventstore.eventsWithUUIDToOccurrenceDateMap_inCalendars_(*args, **kwargs)

    def exposed_bindings(self, *args, **kwargs):
        return self._ekeventstore.exposedBindings(*args, **kwargs)

    def fetch_changed_object_ids_since_token_result_handler_(self, *args, **kwargs):
        return self._ekeventstore.fetchChangedObjectIDsSinceToken_resultHandler_(*args, **kwargs)

    def fetch_changed_object_ids_(self, *args, **kwargs):
        return self._ekeventstore.fetchChangedObjectIDs_(*args, **kwargs)

    def fetch_event_counts_in_range_in_calendars_exclusion_options_completion_(self, *args, **kwargs):
        return self._ekeventstore.fetchEventCountsInRange_inCalendars_exclusionOptions_completion_(*args, **kwargs)

    def fetch_events_matching_predicate_result_handler_(self, *args, **kwargs):
        return self._ekeventstore.fetchEventsMatchingPredicate_resultHandler_(*args, **kwargs)

    def fetch_granted_delegates_for_source_results_(self, *args, **kwargs):
        return self._ekeventstore.fetchGrantedDelegatesForSource_results_(*args, **kwargs)

    def fetch_reminders_matching_predicate_completion_(self, *args, **kwargs):
        return self._ekeventstore.fetchRemindersMatchingPredicate_completion_(*args, **kwargs)

    def fetch_storage_usage(self, *args, **kwargs):
        return self._ekeventstore.fetchStorageUsage(*args, **kwargs)

    def finalize(self, *args, **kwargs):
        return self._ekeventstore.finalize(*args, **kwargs)

    def finish_observing(self, *args, **kwargs):
        return self._ekeventstore.finishObserving(*args, **kwargs)

    def flush_key_bindings(self, *args, **kwargs):
        return self._ekeventstore.flushKeyBindings(*args, **kwargs)

    def forward_invocation_(self, *args, **kwargs):
        return self._ekeventstore.forwardInvocation_(*args, **kwargs)

    def forwarding_target_for_selector_(self, *args, **kwargs):
        return self._ekeventstore.forwardingTargetForSelector_(*args, **kwargs)

    def fp__ivar_description_for_class_(self, *args, **kwargs):
        return self._ekeventstore.fp__ivarDescriptionForClass_(*args, **kwargs)

    def fp__method_description_for_class_(self, *args, **kwargs):
        return self._ekeventstore.fp__methodDescriptionForClass_(*args, **kwargs)

    def fp_ivar_description(self, *args, **kwargs):
        return self._ekeventstore.fp_ivarDescription(*args, **kwargs)

    def fp_method_description(self, *args, **kwargs):
        return self._ekeventstore.fp_methodDescription(*args, **kwargs)

    def fp_short_method_description(self, *args, **kwargs):
        return self._ekeventstore.fp_shortMethodDescription(*args, **kwargs)

    def future_scheduled_events_exist_on_calendar_(self, *args, **kwargs):
        return self._ekeventstore.futureScheduledEventsExistOnCalendar_(*args, **kwargs)

    def get_maps_with_reminder_source_map_event_source_map_(self, *args, **kwargs):
        return self._ekeventstore.getMapsWithReminderSourceMap_eventSourceMap_(*args, **kwargs)

    def get_subscribed_calendars_source_create_if_needed_with_error_(self, *args, **kwargs):
        return self._ekeventstore.getSubscribedCalendarsSourceCreateIfNeededWithError_(*args, **kwargs)

    def handle_external_database_change_notification_(self, *args, **kwargs):
        return self._ekeventstore.handleExternalDatabaseChangeNotification_(*args, **kwargs)

    def handle_query_with_unbound_key_(self, *args, **kwargs):
        return self._ekeventstore.handleQueryWithUnboundKey_(*args, **kwargs)

    def handle_take_value_for_unbound_key_(self, *args, **kwargs):
        return self._ekeventstore.handleTakeValue_forUnboundKey_(*args, **kwargs)

    def has_immediately_eligible_travel_events(self, *args, **kwargs):
        return self._ekeventstore.hasImmediatelyEligibleTravelEvents(*args, **kwargs)

    def hash(self, *args, **kwargs):
        return self._ekeventstore.hash(*args, **kwargs)

    def hide_calendars_from_notification_center_error_(self, *args, **kwargs):
        return self._ekeventstore.hideCalendarsFromNotificationCenter_error_(*args, **kwargs)

    def if_set_value_if_non_nil_for_key_(self, *args, **kwargs):
        return self._ekeventstore.if_setValueIfNonNil_forKey_(*args, **kwargs)

    def if_set_value_if_y_e_s_for_key_(self, *args, **kwargs):
        return self._ekeventstore.if_setValueIfYES_forKey_(*args, **kwargs)

    def ignore_external_changes(self, *args, **kwargs):
        return self._ekeventstore.ignoreExternalChanges(*args, **kwargs)

    def image_cache(self, *args, **kwargs):
        return self._ekeventstore.imageCache(*args, **kwargs)

    def implements_selector_(self, *args, **kwargs):
        return self._ekeventstore.implementsSelector_(*args, **kwargs)

    def import_events_with_external_ids_from_i_c_s_data_into_calendars_options_batch_size_(self, *args, **kwargs):
        return self._ekeventstore.importEventsWithExternalIDs_fromICSData_intoCalendars_options_batchSize_(*args, **kwargs)

    def import_i_c_s_data_into_calendar_options_(self, *args, **kwargs):
        return self._ekeventstore.importICSData_intoCalendar_options_(*args, **kwargs)

    def import_i_c_s_data_into_calendars_options_(self, *args, **kwargs):
        return self._ekeventstore.importICSData_intoCalendars_options_(*args, **kwargs)

    def import_i_c_s_into_calendar_options_(self, *args, **kwargs):
        return self._ekeventstore.importICS_intoCalendar_options_(*args, **kwargs)

    def import_v_c_s_data_into_calendars_error_(self, *args, **kwargs):
        return self._ekeventstore.importVCSData_intoCalendars_error_(*args, **kwargs)

    def inbox_replied_section_has_content(self, *args, **kwargs):
        return self._ekeventstore.inboxRepliedSectionHasContent(*args, **kwargs)

    def inbox_replied_section_items(self, *args, **kwargs):
        return self._ekeventstore.inboxRepliedSectionItems(*args, **kwargs)

    def info_for_binding_(self, *args, **kwargs):
        return self._ekeventstore.infoForBinding_(*args, **kwargs)

    def init(self, *args, **kwargs):
        return self._ekeventstore.init(*args, **kwargs)

    def init_with_access_to_entity_types_(self, *args, **kwargs):
        return self._ekeventstore.initWithAccessToEntityTypes_(*args, **kwargs)

    def init_with_birthday_calendar_modifications(self, *args, **kwargs):
        return self._ekeventstore.initWithBirthdayCalendarModifications(*args, **kwargs)

    def init_with_e_k_options_(self, *args, **kwargs):
        return self._ekeventstore.initWithEKOptions_(*args, **kwargs)

    def init_with_e_k_options_path_change_tracking_client_id_enable_property_modification_logging_allow_delegate_sources_(self, *args, **kwargs):
        return self._ekeventstore.initWithEKOptions_path_changeTrackingClientId_enablePropertyModificationLogging_allowDelegateSources_(*args, **kwargs)

    def init_with_e_k_options_path_change_tracking_client_id_enable_property_modification_logging_allow_delegate_sources_allowed_source_identifiers_(self, *args, **kwargs):
        return self._ekeventstore.initWithEKOptions_path_changeTrackingClientId_enablePropertyModificationLogging_allowDelegateSources_allowedSourceIdentifiers_(*args, **kwargs)

    def init_with_e_k_options_path_conainer_provider_change_tracking_client_id_enable_property_modification_logging_allow_delegate_sources_allowed_source_identifiers_(self, *args, **kwargs):
        return self._ekeventstore.initWithEKOptions_path_conainerProvider_changeTrackingClientId_enablePropertyModificationLogging_allowDelegateSources_allowedSourceIdentifiers_(*args, **kwargs)

    def init_with_e_k_options_path_sources_(self, *args, **kwargs):
        return self._ekeventstore.initWithEKOptions_path_sources_(*args, **kwargs)

    def init_with_options_path_(self, *args, **kwargs):
        return self._ekeventstore.initWithOptions_path_(*args, **kwargs)

    def init_with_options_path_allow_delegate_sources_(self, *args, **kwargs):
        return self._ekeventstore.initWithOptions_path_allowDelegateSources_(*args, **kwargs)

    def init_with_options_path_change_tracking_client_id_enable_property_modification_logging_allow_delegate_sources_(self, *args, **kwargs):
        return self._ekeventstore.initWithOptions_path_changeTrackingClientId_enablePropertyModificationLogging_allowDelegateSources_(*args, **kwargs)

    def init_with_sources_(self, *args, **kwargs):
        return self._ekeventstore.initWithSources_(*args, **kwargs)

    def init_with_store_type_options_(self, *args, **kwargs):
        return self._ekeventstore.initWithStoreType_options_(*args, **kwargs)

    def initialize_e_k_event_store_plus_reminders(self, *args, **kwargs):
        return self._ekeventstore.initializeEKEventStorePlusReminders(*args, **kwargs)

    def insert_suggested_event_calendar(self, *args, **kwargs):
        return self._ekeventstore.insertSuggestedEventCalendar(*args, **kwargs)

    def insert_value_at_index_in_property_with_key_(self, *args, **kwargs):
        return self._ekeventstore.insertValue_atIndex_inPropertyWithKey_(*args, **kwargs)

    def insert_value_in_property_with_key_(self, *args, **kwargs):
        return self._ekeventstore.insertValue_inPropertyWithKey_(*args, **kwargs)

    def inserted_object_ids(self, *args, **kwargs):
        return self._ekeventstore.insertedObjectIDs(*args, **kwargs)

    def inserted_objects(self, *args, **kwargs):
        return self._ekeventstore.insertedObjects(*args, **kwargs)

    def inserted_persistent_object_with_entity_name_(self, *args, **kwargs):
        return self._ekeventstore.insertedPersistentObjectWithEntityName_(*args, **kwargs)

    def int64_value_safe(self, *args, **kwargs):
        return self._ekeventstore.int64ValueSafe(*args, **kwargs)

    def int64_value_safe_(self, *args, **kwargs):
        return self._ekeventstore.int64ValueSafe_(*args, **kwargs)

    def invalidate_reminder_source_maps(self, *args, **kwargs):
        return self._ekeventstore.invalidateReminderSourceMaps(*args, **kwargs)

    def inverse_for_relationship_key_(self, *args, **kwargs):
        return self._ekeventstore.inverseForRelationshipKey_(*args, **kwargs)

    def is_case_insensitive_like_(self, *args, **kwargs):
        return self._ekeventstore.isCaseInsensitiveLike_(*args, **kwargs)

    def is_current_process_creator_of_event_(self, *args, **kwargs):
        return self._ekeventstore.isCurrentProcessCreatorOfEvent_(*args, **kwargs)

    def is_data_protected(self, *args, **kwargs):
        return self._ekeventstore.isDataProtected(*args, **kwargs)

    def is_equal_to_(self, *args, **kwargs):
        return self._ekeventstore.isEqualTo_(*args, **kwargs)

    def is_equal_(self, *args, **kwargs):
        return self._ekeventstore.isEqual_(*args, **kwargs)

    def is_fault(self, *args, **kwargs):
        return self._ekeventstore.isFault(*args, **kwargs)

    def is_greater_than_or_equal_to_(self, *args, **kwargs):
        return self._ekeventstore.isGreaterThanOrEqualTo_(*args, **kwargs)

    def is_greater_than_(self, *args, **kwargs):
        return self._ekeventstore.isGreaterThan_(*args, **kwargs)

    def is_kind_of_class_(self, *args, **kwargs):
        return self._ekeventstore.isKindOfClass_(*args, **kwargs)

    def is_less_than_or_equal_to_(self, *args, **kwargs):
        return self._ekeventstore.isLessThanOrEqualTo_(*args, **kwargs)

    def is_less_than_(self, *args, **kwargs):
        return self._ekeventstore.isLessThan_(*args, **kwargs)

    def is_like_(self, *args, **kwargs):
        return self._ekeventstore.isLike_(*args, **kwargs)

    def is_member_of_class_(self, *args, **kwargs):
        return self._ekeventstore.isMemberOfClass_(*args, **kwargs)

    def is_n_s_array__(self, *args, **kwargs):
        return self._ekeventstore.isNSArray__(*args, **kwargs)

    def is_n_s_c_f_constant_string__(self, *args, **kwargs):
        return self._ekeventstore.isNSCFConstantString__(*args, **kwargs)

    def is_n_s_data__(self, *args, **kwargs):
        return self._ekeventstore.isNSData__(*args, **kwargs)

    def is_n_s_date__(self, *args, **kwargs):
        return self._ekeventstore.isNSDate__(*args, **kwargs)

    def is_n_s_dictionary__(self, *args, **kwargs):
        return self._ekeventstore.isNSDictionary__(*args, **kwargs)

    def is_n_s_number__(self, *args, **kwargs):
        return self._ekeventstore.isNSNumber__(*args, **kwargs)

    def is_n_s_object__(self, *args, **kwargs):
        return self._ekeventstore.isNSObject__(*args, **kwargs)

    def is_n_s_ordered_set__(self, *args, **kwargs):
        return self._ekeventstore.isNSOrderedSet__(*args, **kwargs)

    def is_n_s_set__(self, *args, **kwargs):
        return self._ekeventstore.isNSSet__(*args, **kwargs)

    def is_n_s_string__(self, *args, **kwargs):
        return self._ekeventstore.isNSString__(*args, **kwargs)

    def is_n_s_time_zone__(self, *args, **kwargs):
        return self._ekeventstore.isNSTimeZone__(*args, **kwargs)

    def is_n_s_value__(self, *args, **kwargs):
        return self._ekeventstore.isNSValue__(*args, **kwargs)

    def is_not_equal_to_(self, *args, **kwargs):
        return self._ekeventstore.isNotEqualTo_(*args, **kwargs)

    def is_null(self, *args, **kwargs):
        return self._ekeventstore.isNull(*args, **kwargs)

    def is_object_inserted_(self, *args, **kwargs):
        return self._ekeventstore.isObjectInserted_(*args, **kwargs)

    def is_proxy(self, *args, **kwargs):
        return self._ekeventstore.isProxy(*args, **kwargs)

    def is_source_managed_(self, *args, **kwargs):
        return self._ekeventstore.isSourceManaged_(*args, **kwargs)

    def is_to_many_key_(self, *args, **kwargs):
        return self._ekeventstore.isToManyKey_(*args, **kwargs)

    def key_value_binding_for_key_type_mask_(self, *args, **kwargs):
        return self._ekeventstore.keyValueBindingForKey_typeMask_(*args, **kwargs)

    def last_commit_temp_to_permanent_object_id_map(self, *args, **kwargs):
        return self._ekeventstore.lastCommitTempToPermanentObjectIDMap(*args, **kwargs)

    def last_confirmed_splash_screen_version(self, *args, **kwargs):
        return self._ekeventstore.lastConfirmedSplashScreenVersion(*args, **kwargs)

    def last_database_notification_timestamp(self, *args, **kwargs):
        return self._ekeventstore.lastDatabaseNotificationTimestamp(*args, **kwargs)

    def last_database_timestamp_for_o_o_p_to_wait_on(self, *args, **kwargs):
        return self._ekeventstore.lastDatabaseTimestampForOOPToWaitOn(*args, **kwargs)

    def load_draft_of_event_with_occurrence_id_(self, *args, **kwargs):
        return self._ekeventstore.loadDraftOfEventWithOccurrenceID_(*args, **kwargs)

    def local_birthday_calendar_create_if_needed_with_error_(self, *args, **kwargs):
        return self._ekeventstore.localBirthdayCalendarCreateIfNeededWithError_(*args, **kwargs)

    def local_birthday_calendar_source(self, *args, **kwargs):
        return self._ekeventstore.localBirthdayCalendarSource(*args, **kwargs)

    def local_source(self, *args, **kwargs):
        return self._ekeventstore.localSource(*args, **kwargs)

    def local_source_enable_if_needed(self, *args, **kwargs):
        return self._ekeventstore.localSourceEnableIfNeeded(*args, **kwargs)

    def mark_changed_object_ids_consumed_up_to_token_(self, *args, **kwargs):
        return self._ekeventstore.markChangedObjectIDsConsumedUpToToken_(*args, **kwargs)

    def mark_individual_changes_consumed_error_(self, *args, **kwargs):
        return self._ekeventstore.markIndividualChangesConsumed_error_(*args, **kwargs)

    def mark_resource_change_alerted_and_save_error_(self, *args, **kwargs):
        return self._ekeventstore.markResourceChangeAlertedAndSave_error_(*args, **kwargs)

    def method_description_for_selector_(self, *args, **kwargs):
        return self._ekeventstore.methodDescriptionForSelector_(*args, **kwargs)

    def method_for_selector_(self, *args, **kwargs):
        return self._ekeventstore.methodForSelector_(*args, **kwargs)

    def method_signature_for_selector_(self, *args, **kwargs):
        return self._ekeventstore.methodSignatureForSelector_(*args, **kwargs)

    def mimic_save_and_commit_event_old_to_new_object_id_map_inserted_object_ids_updated_object_ids_deleted_object_ids_(self, *args, **kwargs):
        return self._ekeventstore.mimicSaveAndCommitEvent_oldToNewObjectIDMap_insertedObjectIDs_updatedObjectIDs_deletedObjectIDs_(*args, **kwargs)

    def mr_formatted_debug_description(self, *args, **kwargs):
        return self._ekeventstore.mr_formattedDebugDescription(*args, **kwargs)

    def mutable_array_value_for_key_path_(self, *args, **kwargs):
        return self._ekeventstore.mutableArrayValueForKeyPath_(*args, **kwargs)

    def mutable_array_value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.mutableArrayValueForKey_(*args, **kwargs)

    def mutable_copy(self, *args, **kwargs):
        return self._ekeventstore.mutableCopy(*args, **kwargs)

    def mutable_ordered_set_value_for_key_path_(self, *args, **kwargs):
        return self._ekeventstore.mutableOrderedSetValueForKeyPath_(*args, **kwargs)

    def mutable_ordered_set_value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.mutableOrderedSetValueForKey_(*args, **kwargs)

    def mutable_set_value_for_key_path_(self, *args, **kwargs):
        return self._ekeventstore.mutableSetValueForKeyPath_(*args, **kwargs)

    def mutable_set_value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.mutableSetValueForKey_(*args, **kwargs)

    def natural_language_suggested_event_calendar(self, *args, **kwargs):
        return self._ekeventstore.naturalLanguageSuggestedEventCalendar(*args, **kwargs)

    def needs_geocoding_for_event_(self, *args, **kwargs):
        return self._ekeventstore.needsGeocodingForEvent_(*args, **kwargs)

    def new_scripting_object_of_class_for_value_for_key_with_contents_value_properties_(self, *args, **kwargs):
        return self._ekeventstore.newScriptingObjectOfClass_forValueForKey_withContentsValue_properties_(*args, **kwargs)

    def new_tagged_n_s_string_with_a_s_c_i_i_bytes__length__(self, *args, **kwargs):
        return self._ekeventstore.newTaggedNSStringWithASCIIBytes__length__(*args, **kwargs)

    def next_event_with_calendar_identifiers_exclusion_options_(self, *args, **kwargs):
        return self._ekeventstore.nextEventWithCalendarIdentifiers_exclusionOptions_(*args, **kwargs)

    def next_event_with_calendars_exclusion_options_(self, *args, **kwargs):
        return self._ekeventstore.nextEventWithCalendars_exclusionOptions_(*args, **kwargs)

    def next_events_with_calendars_limit_exclusion_options_(self, *args, **kwargs):
        return self._ekeventstore.nextEventsWithCalendars_limit_exclusionOptions_(*args, **kwargs)

    def notification_collection_cache_queue(self, *args, **kwargs):
        return self._ekeventstore.notificationCollectionCacheQueue(*args, **kwargs)

    def notification_collection_for_source_(self, *args, **kwargs):
        return self._ekeventstore.notificationCollectionForSource_(*args, **kwargs)

    def object_specifier(self, *args, **kwargs):
        return self._ekeventstore.objectSpecifier(*args, **kwargs)

    def object_with_id_exists_(self, *args, **kwargs):
        return self._ekeventstore.objectWithIDExists_(*args, **kwargs)

    def object_with_object_id_(self, *args, **kwargs):
        return self._ekeventstore.objectWithObjectID_(*args, **kwargs)

    def objects_have_changes_to_commit_(self, *args, **kwargs):
        return self._ekeventstore.objectsHaveChangesToCommit_(*args, **kwargs)

    def objects_matching_predicate_(self, *args, **kwargs):
        return self._ekeventstore.objectsMatchingPredicate_(*args, **kwargs)

    def objects_pending_commit(self, *args, **kwargs):
        return self._ekeventstore.objectsPendingCommit(*args, **kwargs)

    def objects_pending_save(self, *args, **kwargs):
        return self._ekeventstore.objectsPendingSave(*args, **kwargs)

    def observation_info(self, *args, **kwargs):
        return self._ekeventstore.observationInfo(*args, **kwargs)

    def observe_value_for_key_path_of_object_change_context_(self, *args, **kwargs):
        return self._ekeventstore.observeValueForKeyPath_ofObject_change_context_(*args, **kwargs)

    def occurrence_cache_get_occurrence_counts_for_calendars_(self, *args, **kwargs):
        return self._ekeventstore.occurrenceCacheGetOccurrenceCountsForCalendars_(*args, **kwargs)

    def occurrence_cache_get_occurrences_for_calendars_on_day_(self, *args, **kwargs):
        return self._ekeventstore.occurrenceCacheGetOccurrencesForCalendars_onDay_(*args, **kwargs)

    def occurrences_exist_in_range_for_event_start_date_end_date_must_start_in_interval_timezone_(self, *args, **kwargs):
        return self._ekeventstore.occurrencesExistInRangeForEvent_startDate_endDate_mustStartInInterval_timezone_(*args, **kwargs)

    def option_descriptions_for_binding_(self, *args, **kwargs):
        return self._ekeventstore.optionDescriptionsForBinding_(*args, **kwargs)

    def owns_destination_objects_for_relationship_key_(self, *args, **kwargs):
        return self._ekeventstore.ownsDestinationObjectsForRelationshipKey_(*args, **kwargs)

    def parent_source_for_delegate_source_(self, *args, **kwargs):
        return self._ekeventstore.parentSourceForDelegateSource_(*args, **kwargs)

    def pep_after_delay_(self, *args, **kwargs):
        return self._ekeventstore.pep_afterDelay_(*args, **kwargs)

    def pep_get_invocation_(self, *args, **kwargs):
        return self._ekeventstore.pep_getInvocation_(*args, **kwargs)

    def pep_on_main_thread(self, *args, **kwargs):
        return self._ekeventstore.pep_onMainThread(*args, **kwargs)

    def pep_on_main_thread_if_necessary(self, *args, **kwargs):
        return self._ekeventstore.pep_onMainThreadIfNecessary(*args, **kwargs)

    def pep_on_operation_queue_(self, *args, **kwargs):
        return self._ekeventstore.pep_onOperationQueue_(*args, **kwargs)

    def pep_on_operation_queue_priority_(self, *args, **kwargs):
        return self._ekeventstore.pep_onOperationQueue_priority_(*args, **kwargs)

    def pep_on_thread_(self, *args, **kwargs):
        return self._ekeventstore.pep_onThread_(*args, **kwargs)

    def pep_on_thread_immediate_for_matching_thread_(self, *args, **kwargs):
        return self._ekeventstore.pep_onThread_immediateForMatchingThread_(*args, **kwargs)

    def perform_block_on_main_thread_synchronously_(self, *args, **kwargs):
        return self._ekeventstore.performBlockOnMainThreadSynchronously_(*args, **kwargs)

    def perform_holding_reminder_source_map_lock_(self, *args, **kwargs):
        return self._ekeventstore.performHoldingReminderSourceMapLock_(*args, **kwargs)

    def perform_selector_in_background_with_object_(self, *args, **kwargs):
        return self._ekeventstore.performSelectorInBackground_withObject_(*args, **kwargs)

    def perform_selector_on_main_thread_with_object_wait_until_done_(self, *args, **kwargs):
        return self._ekeventstore.performSelectorOnMainThread_withObject_waitUntilDone_(*args, **kwargs)

    def perform_selector_on_main_thread_with_object_wait_until_done_modes_(self, *args, **kwargs):
        return self._ekeventstore.performSelectorOnMainThread_withObject_waitUntilDone_modes_(*args, **kwargs)

    def perform_selector_(self, *args, **kwargs):
        return self._ekeventstore.performSelector_(*args, **kwargs)

    def perform_selector_object_after_delay_(self, *args, **kwargs):
        return self._ekeventstore.performSelector_object_afterDelay_(*args, **kwargs)

    def perform_selector_on_thread_with_object_wait_until_done_(self, *args, **kwargs):
        return self._ekeventstore.performSelector_onThread_withObject_waitUntilDone_(*args, **kwargs)

    def perform_selector_on_thread_with_object_wait_until_done_modes_(self, *args, **kwargs):
        return self._ekeventstore.performSelector_onThread_withObject_waitUntilDone_modes_(*args, **kwargs)

    def perform_selector_with_object_(self, *args, **kwargs):
        return self._ekeventstore.performSelector_withObject_(*args, **kwargs)

    def perform_selector_with_object_after_delay_(self, *args, **kwargs):
        return self._ekeventstore.performSelector_withObject_afterDelay_(*args, **kwargs)

    def perform_selector_with_object_after_delay_ignore_menu_tracking_(self, *args, **kwargs):
        return self._ekeventstore.performSelector_withObject_afterDelay_ignoreMenuTracking_(*args, **kwargs)

    def perform_selector_with_object_after_delay_in_modes_(self, *args, **kwargs):
        return self._ekeventstore.performSelector_withObject_afterDelay_inModes_(*args, **kwargs)

    def perform_selector_with_object_with_object_(self, *args, **kwargs):
        return self._ekeventstore.performSelector_withObject_withObject_(*args, **kwargs)

    def persistent_object_with_entity_name_(self, *args, **kwargs):
        return self._ekeventstore.persistentObjectWithEntityName_(*args, **kwargs)

    def post_synthetic_route_hypothesis_for_event_with_external_u_r_l_(self, *args, **kwargs):
        return self._ekeventstore.postSyntheticRouteHypothesis_forEventWithExternalURL_(*args, **kwargs)

    def predicate_for_assistant_event_search_with_time_zone_start_date_end_date_title_location_notes_participants_calendars_limit_(self, *args, **kwargs):
        return self._ekeventstore.predicateForAssistantEventSearchWithTimeZone_startDate_endDate_title_location_notes_participants_calendars_limit_(*args, **kwargs)

    def predicate_for_calendar_items_of_type_in_calendar_(self, *args, **kwargs):
        return self._ekeventstore.predicateForCalendarItemsOfType_inCalendar_(*args, **kwargs)

    def predicate_for_calendar_items_of_type_with_external_id_in_calendar_(self, *args, **kwargs):
        return self._ekeventstore.predicateForCalendarItemsOfType_withExternalID_inCalendar_(*args, **kwargs)

    def predicate_for_calendar_items_of_type_with_external_id_in_source_(self, *args, **kwargs):
        return self._ekeventstore.predicateForCalendarItemsOfType_withExternalID_inSource_(*args, **kwargs)

    def predicate_for_calendar_items_of_type_with_unique_identifier_in_calendar_(self, *args, **kwargs):
        return self._ekeventstore.predicateForCalendarItemsOfType_withUniqueIdentifier_inCalendar_(*args, **kwargs)

    def predicate_for_calendar_items_of_type_with_unique_identifier_in_source_(self, *args, **kwargs):
        return self._ekeventstore.predicateForCalendarItemsOfType_withUniqueIdentifier_inSource_(*args, **kwargs)

    def predicate_for_calendar_store_for_reminders_in_calendars_(self, *args, **kwargs):
        return self._ekeventstore.predicateForCalendarStoreForRemindersInCalendars_(*args, **kwargs)

    def predicate_for_completed_reminders_with_completion_date_starting_ending_calendars_(self, *args, **kwargs):
        return self._ekeventstore.predicateForCompletedRemindersWithCompletionDateStarting_ending_calendars_(*args, **kwargs)

    def predicate_for_event_created_from_suggestion_with_opaque_key_(self, *args, **kwargs):
        return self._ekeventstore.predicateForEventCreatedFromSuggestionWithOpaqueKey_(*args, **kwargs)

    def predicate_for_events_created_from_suggestion(self, *args, **kwargs):
        return self._ekeventstore.predicateForEventsCreatedFromSuggestion(*args, **kwargs)

    def predicate_for_events_created_from_suggestion_with_extraction_group_identifier_(self, *args, **kwargs):
        return self._ekeventstore.predicateForEventsCreatedFromSuggestionWithExtractionGroupIdentifier_(*args, **kwargs)

    def predicate_for_events_in_subscribed_calendar_(self, *args, **kwargs):
        return self._ekeventstore.predicateForEventsInSubscribedCalendar_(*args, **kwargs)

    def predicate_for_events_with_attendees_in_calendar_(self, *args, **kwargs):
        return self._ekeventstore.predicateForEventsWithAttendeesInCalendar_(*args, **kwargs)

    def predicate_for_events_with_conference_u_r_l_limit_(self, *args, **kwargs):
        return self._ekeventstore.predicateForEventsWithConferenceURL_limit_(*args, **kwargs)

    def predicate_for_events_with_start_date_end_date_calendars_(self, *args, **kwargs):
        return self._ekeventstore.predicateForEventsWithStartDate_endDate_calendars_(*args, **kwargs)

    def predicate_for_events_with_start_date_end_date_calendars_exclusion_options_filterd_out_titles_randomize_limit_(self, *args, **kwargs):
        return self._ekeventstore.predicateForEventsWithStartDate_endDate_calendars_exclusionOptions_filterdOutTitles_randomize_limit_(*args, **kwargs)

    def predicate_for_events_with_start_date_end_date_calendars_load_default_properties_(self, *args, **kwargs):
        return self._ekeventstore.predicateForEventsWithStartDate_endDate_calendars_loadDefaultProperties_(*args, **kwargs)

    def predicate_for_events_with_start_date_end_date_calendars_matching_contacts_(self, *args, **kwargs):
        return self._ekeventstore.predicateForEventsWithStartDate_endDate_calendars_matchingContacts_(*args, **kwargs)

    def predicate_for_events_with_start_date_end_date_calendars_prefetch_hint_exclusion_options_(self, *args, **kwargs):
        return self._ekeventstore.predicateForEventsWithStartDate_endDate_calendars_prefetchHint_exclusionOptions_(*args, **kwargs)

    def predicate_for_events_with_start_date_end_date_unique_id_calendars_(self, *args, **kwargs):
        return self._ekeventstore.predicateForEventsWithStartDate_endDate_uniqueID_calendars_(*args, **kwargs)

    def predicate_for_incomplete_reminders_with_due_date_starting_ending_calendars_(self, *args, **kwargs):
        return self._ekeventstore.predicateForIncompleteRemindersWithDueDateStarting_ending_calendars_(*args, **kwargs)

    def predicate_for_master_events_in_calendar_(self, *args, **kwargs):
        return self._ekeventstore.predicateForMasterEventsInCalendar_(*args, **kwargs)

    def predicate_for_master_events_in_calendars_(self, *args, **kwargs):
        return self._ekeventstore.predicateForMasterEventsInCalendars_(*args, **kwargs)

    def predicate_for_master_events_with_external_tracking_status_in_calendar_(self, *args, **kwargs):
        return self._ekeventstore.predicateForMasterEventsWithExternalTrackingStatusInCalendar_(*args, **kwargs)

    def predicate_for_master_events_with_invitations_and_occurrences_after_in_calendar_(self, *args, **kwargs):
        return self._ekeventstore.predicateForMasterEventsWithInvitationsAndOccurrencesAfter_inCalendar_(*args, **kwargs)

    def predicate_for_master_events_with_occurrences_with_start_date_end_date_in_calendar_(self, *args, **kwargs):
        return self._ekeventstore.predicateForMasterEventsWithOccurrencesWithStartDate_endDate_inCalendar_(*args, **kwargs)

    def predicate_for_master_events_with_start_date_title_in_calendar_(self, *args, **kwargs):
        return self._ekeventstore.predicateForMasterEventsWithStartDate_title_inCalendar_(*args, **kwargs)

    def predicate_for_natural_language_suggested_events_with_search_string_(self, *args, **kwargs):
        return self._ekeventstore.predicateForNaturalLanguageSuggestedEventsWithSearchString_(*args, **kwargs)

    def predicate_for_natural_language_suggested_events_with_search_string_start_date_(self, *args, **kwargs):
        return self._ekeventstore.predicateForNaturalLanguageSuggestedEventsWithSearchString_startDate_(*args, **kwargs)

    def predicate_for_nonrecurring_events_with_start_date_end_date_calendars_(self, *args, **kwargs):
        return self._ekeventstore.predicateForNonrecurringEventsWithStartDate_endDate_calendars_(*args, **kwargs)

    def predicate_for_notifiable_events(self, *args, **kwargs):
        return self._ekeventstore.predicateForNotifiableEvents(*args, **kwargs)

    def predicate_for_notification_center_visible_events(self, *args, **kwargs):
        return self._ekeventstore.predicateForNotificationCenterVisibleEvents(*args, **kwargs)

    def predicate_for_potential_travel_events_in_calendars_start_date_end_date_(self, *args, **kwargs):
        return self._ekeventstore.predicateForPotentialTravelEventsInCalendars_startDate_endDate_(*args, **kwargs)

    def predicate_for_random_master_events_with_start_date_end_date_need_to_have_attendee_need_to_have_location_all_day_filtered_out_titles_limit_calendars_(self, *args, **kwargs):
        return self._ekeventstore.predicateForRandomMasterEventsWithStartDate_endDate_needToHaveAttendee_needToHaveLocation_allDay_filteredOutTitles_limit_calendars_(*args, **kwargs)

    def predicate_for_reminders_in_calendars_(self, *args, **kwargs):
        return self._ekeventstore.predicateForRemindersInCalendars_(*args, **kwargs)

    def predicate_for_reminders_in_calendars_preload_properties_(self, *args, **kwargs):
        return self._ekeventstore.predicateForRemindersInCalendars_preloadProperties_(*args, **kwargs)

    def predicate_for_reminders_with_title_list_title_limit_to_completed_or_incomplete_completed_due_after_due_before_search_term_sort_order_max_results_(self, *args, **kwargs):
        return self._ekeventstore.predicateForRemindersWithTitle_listTitle_limitToCompletedOrIncomplete_completed_dueAfter_dueBefore_searchTerm_sortOrder_maxResults_(*args, **kwargs)

    def predicate_for_schedule_agent_client_events_in_calendar_(self, *args, **kwargs):
        return self._ekeventstore.predicateForScheduleAgentClientEventsInCalendar_(*args, **kwargs)

    def predicate_for_unacknowledged_events(self, *args, **kwargs):
        return self._ekeventstore.predicateForUnacknowledgedEvents(*args, **kwargs)

    def predicate_for_unalerted_events(self, *args, **kwargs):
        return self._ekeventstore.predicateForUnalertedEvents(*args, **kwargs)

    def predicate_for_up_next_events_in_calendars_start_date_end_date_start_date_restriction_threshold_(self, *args, **kwargs):
        return self._ekeventstore.predicateForUpNextEventsInCalendars_startDate_endDate_startDateRestrictionThreshold_(*args, **kwargs)

    def predicate_for_upcoming_events_with_limit_(self, *args, **kwargs):
        return self._ekeventstore.predicateForUpcomingEventsWithLimit_(*args, **kwargs)

    def prepare_for_interface_builder(self, *args, **kwargs):
        return self._ekeventstore.prepareForInterfaceBuilder(*args, **kwargs)

    def public_object_with_fetched_object_id_(self, *args, **kwargs):
        return self._ekeventstore.publicObjectWithFetchedObjectID_(*args, **kwargs)

    def public_object_with_object_id_(self, *args, **kwargs):
        return self._ekeventstore.publicObjectWithObjectID_(*args, **kwargs)

    def public_object_with_persistent_object_(self, *args, **kwargs):
        return self._ekeventstore.publicObjectWithPersistentObject_(*args, **kwargs)

    def purge_changelog(self, *args, **kwargs):
        return self._ekeventstore.purgeChangelog(*args, **kwargs)

    def read_write_calendar_count_for_entity_type_(self, *args, **kwargs):
        return self._ekeventstore.readWriteCalendarCountForEntityType_(*args, **kwargs)

    def read_write_calendars_for_entity_type_(self, *args, **kwargs):
        return self._ekeventstore.readWriteCalendarsForEntityType_(*args, **kwargs)

    def rebuild_occurrence_cache(self, *args, **kwargs):
        return self._ekeventstore.rebuildOccurrenceCache(*args, **kwargs)

    def receive_observed_error_(self, *args, **kwargs):
        return self._ekeventstore.receiveObservedError_(*args, **kwargs)

    def receive_observed_value_(self, *args, **kwargs):
        return self._ekeventstore.receiveObservedValue_(*args, **kwargs)

    def record_object_rebase_with_old_object_id_new_object_id_(self, *args, **kwargs):
        return self._ekeventstore.recordObjectRebaseWithOldObjectID_newObjectID_(*args, **kwargs)

    def record_sequence_token_for_legacy_clients_(self, *args, **kwargs):
        return self._ekeventstore.recordSequenceTokenForLegacyClients_(*args, **kwargs)

    def redacted_mimic_save_event_old_to_new_object_id_map_serialized_dictionary_object_id_to_change_set_dictionary_map_object_id_to_persistent_dictionary_map_(self, *args, **kwargs):
        return self._ekeventstore.redactedMimicSaveEvent_oldToNewObjectIDMap_serializedDictionary_objectIDToChangeSetDictionaryMap_objectIDToPersistentDictionaryMap_(*args, **kwargs)

    def refresh_everything_if_necessary_(self, *args, **kwargs):
        return self._ekeventstore.refreshEverythingIfNecessary_(*args, **kwargs)

    def refresh_folder_lists_if_necessary_(self, *args, **kwargs):
        return self._ekeventstore.refreshFolderListsIfNecessary_(*args, **kwargs)

    def refresh_source_user_requested_(self, *args, **kwargs):
        return self._ekeventstore.refreshSource_userRequested_(*args, **kwargs)

    def refresh_sources_if_necessary(self, *args, **kwargs):
        return self._ekeventstore.refreshSourcesIfNecessary(*args, **kwargs)

    def refresh_sources_if_necessary_(self, *args, **kwargs):
        return self._ekeventstore.refreshSourcesIfNecessary_(*args, **kwargs)

    def register_fetched_object_with_id_(self, *args, **kwargs):
        return self._ekeventstore.registerFetchedObjectWithID_(*args, **kwargs)

    def register_fetched_object_with_id_with_default_loaded_property_keys_values_(self, *args, **kwargs):
        return self._ekeventstore.registerFetchedObjectWithID_withDefaultLoadedPropertyKeys_values_(*args, **kwargs)

    def register_for_detailed_change_tracking_in_source_error_(self, *args, **kwargs):
        return self._ekeventstore.registerForDetailedChangeTrackingInSource_error_(*args, **kwargs)

    def register_for_detailed_change_tracking_(self, *args, **kwargs):
        return self._ekeventstore.registerForDetailedChangeTracking_(*args, **kwargs)

    def registered_objects(self, *args, **kwargs):
        return self._ekeventstore.registeredObjects(*args, **kwargs)

    def registered_queue(self, *args, **kwargs):
        return self._ekeventstore.registeredQueue(*args, **kwargs)

    def release(self, *args, **kwargs):
        return self._ekeventstore.release(*args, **kwargs)

    def reminder_source_for_event_source_(self, *args, **kwargs):
        return self._ekeventstore.reminderSourceForEventSource_(*args, **kwargs)

    def reminder_source_id_to_event_source_id_mapping(self, *args, **kwargs):
        return self._ekeventstore.reminderSourceIDToEventSourceIDMapping(*args, **kwargs)

    def reminder_source_map(self, *args, **kwargs):
        return self._ekeventstore.reminderSourceMap(*args, **kwargs)

    def reminder_source_map_lock(self, *args, **kwargs):
        return self._ekeventstore.reminderSourceMapLock(*args, **kwargs)

    def reminder_sources(self, *args, **kwargs):
        return self._ekeventstore.reminderSources(*args, **kwargs)

    def reminder_store(self, *args, **kwargs):
        return self._ekeventstore.reminderStore(*args, **kwargs)

    def reminder_store_changed(self, *args, **kwargs):
        return self._ekeventstore.reminderStoreChanged(*args, **kwargs)

    def reminder_with_external_u_r_i_(self, *args, **kwargs):
        return self._ekeventstore.reminderWithExternalURI_(*args, **kwargs)

    def reminder_with_identifier_(self, *args, **kwargs):
        return self._ekeventstore.reminderWithIdentifier_(*args, **kwargs)

    def reminder_with_unique_id_(self, *args, **kwargs):
        return self._ekeventstore.reminderWithUniqueId_(*args, **kwargs)

    def reminders_matching_predicate_(self, *args, **kwargs):
        return self._ekeventstore.remindersMatchingPredicate_(*args, **kwargs)

    def reminders_with_external_identifier_in_calendars_(self, *args, **kwargs):
        return self._ekeventstore.remindersWithExternalIdentifier_inCalendars_(*args, **kwargs)

    def remove_calendar_commit_error_(self, *args, **kwargs):
        return self._ekeventstore.removeCalendar_commit_error_(*args, **kwargs)

    def remove_calendar_error_(self, *args, **kwargs):
        return self._ekeventstore.removeCalendar_error_(*args, **kwargs)

    def remove_event_span_commit_error_(self, *args, **kwargs):
        return self._ekeventstore.removeEvent_span_commit_error_(*args, **kwargs)

    def remove_event_span_error_(self, *args, **kwargs):
        return self._ekeventstore.removeEvent_span_error_(*args, **kwargs)

    def remove_exchange_delegate_completion_(self, *args, **kwargs):
        return self._ekeventstore.removeExchangeDelegate_completion_(*args, **kwargs)

    def remove_invite_reply_notification_error_(self, *args, **kwargs):
        return self._ekeventstore.removeInviteReplyNotification_error_(*args, **kwargs)

    def remove_invite_reply_notifications_error_(self, *args, **kwargs):
        return self._ekeventstore.removeInviteReplyNotifications_error_(*args, **kwargs)

    def remove_object_from_both_sides_of_relationship_with_key_(self, *args, **kwargs):
        return self._ekeventstore.removeObject_fromBothSidesOfRelationshipWithKey_(*args, **kwargs)

    def remove_object_from_property_with_key_(self, *args, **kwargs):
        return self._ekeventstore.removeObject_fromPropertyWithKey_(*args, **kwargs)

    def remove_observation_(self, *args, **kwargs):
        return self._ekeventstore.removeObservation_(*args, **kwargs)

    def remove_observation_for_observable_key_path_(self, *args, **kwargs):
        return self._ekeventstore.removeObservation_forObservableKeyPath_(*args, **kwargs)

    def remove_observer_for_key_path_(self, *args, **kwargs):
        return self._ekeventstore.removeObserver_forKeyPath_(*args, **kwargs)

    def remove_observer_for_key_path_context_(self, *args, **kwargs):
        return self._ekeventstore.removeObserver_forKeyPath_context_(*args, **kwargs)

    def remove_reminder_commit_error_(self, *args, **kwargs):
        return self._ekeventstore.removeReminder_commit_error_(*args, **kwargs)

    def remove_reminder_error_(self, *args, **kwargs):
        return self._ekeventstore.removeReminder_error_(*args, **kwargs)

    def remove_resource_change_error_(self, *args, **kwargs):
        return self._ekeventstore.removeResourceChange_error_(*args, **kwargs)

    def remove_resource_changes_for_calendar_item_error_(self, *args, **kwargs):
        return self._ekeventstore.removeResourceChangesForCalendarItem_error_(*args, **kwargs)

    def remove_resource_changes_error_(self, *args, **kwargs):
        return self._ekeventstore.removeResourceChanges_error_(*args, **kwargs)

    def remove_source_commit_error_(self, *args, **kwargs):
        return self._ekeventstore.removeSource_commit_error_(*args, **kwargs)

    def remove_suggested_event_calendar(self, *args, **kwargs):
        return self._ekeventstore.removeSuggestedEventCalendar(*args, **kwargs)

    def remove_value_at_index_from_property_with_key_(self, *args, **kwargs):
        return self._ekeventstore.removeValueAtIndex_fromPropertyWithKey_(*args, **kwargs)

    def replace_value_at_index_in_property_with_key_with_value_(self, *args, **kwargs):
        return self._ekeventstore.replaceValueAtIndex_inPropertyWithKey_withValue_(*args, **kwargs)

    def replacement_object_for_archiver_(self, *args, **kwargs):
        return self._ekeventstore.replacementObjectForArchiver_(*args, **kwargs)

    def replacement_object_for_coder_(self, *args, **kwargs):
        return self._ekeventstore.replacementObjectForCoder_(*args, **kwargs)

    def replacement_object_for_keyed_archiver_(self, *args, **kwargs):
        return self._ekeventstore.replacementObjectForKeyedArchiver_(*args, **kwargs)

    def replacement_object_for_port_coder_(self, *args, **kwargs):
        return self._ekeventstore.replacementObjectForPortCoder_(*args, **kwargs)

    def request_access_to_entity_type_completion_(self, *args, **kwargs):
        return self._ekeventstore.requestAccessToEntityType_completion_(*args, **kwargs)

    def request_access_to_entity_type_desired_full_access_testing_synchronous_reason_completion_(self, *args, **kwargs):
        return self._ekeventstore.requestAccessToEntityType_desiredFullAccess_testing_synchronous_reason_completion_(*args, **kwargs)

    def request_full_access_to_events_with_completion_(self, *args, **kwargs):
        return self._ekeventstore.requestFullAccessToEventsWithCompletion_(*args, **kwargs)

    def request_full_access_to_reminders_with_completion_(self, *args, **kwargs):
        return self._ekeventstore.requestFullAccessToRemindersWithCompletion_(*args, **kwargs)

    def request_write_only_access_to_events_with_completion_(self, *args, **kwargs):
        return self._ekeventstore.requestWriteOnlyAccessToEventsWithCompletion_(*args, **kwargs)

    def reset(self, *args, **kwargs):
        return self._ekeventstore.reset(*args, **kwargs)

    def reset_cache(self, *args, **kwargs):
        return self._ekeventstore.resetCache(*args, **kwargs)

    def resource_changes_for_entity_types_(self, *args, **kwargs):
        return self._ekeventstore.resourceChangesForEntityTypes_(*args, **kwargs)

    def respond_to_shared_calendar_invitation_with_status_(self, *args, **kwargs):
        return self._ekeventstore.respondToSharedCalendarInvitation_withStatus_(*args, **kwargs)

    def responds_to_selector_(self, *args, **kwargs):
        return self._ekeventstore.respondsToSelector_(*args, **kwargs)

    def restore_database_from_backup_with_format_error_(self, *args, **kwargs):
        return self._ekeventstore.restoreDatabaseFromBackup_withFormat_error_(*args, **kwargs)

    def restore_generation_changed(self, *args, **kwargs):
        return self._ekeventstore.restoreGenerationChanged(*args, **kwargs)

    def retain(self, *args, **kwargs):
        return self._ekeventstore.retain(*args, **kwargs)

    def retain_count(self, *args, **kwargs):
        return self._ekeventstore.retainCount(*args, **kwargs)

    def retain_weak_reference(self, *args, **kwargs):
        return self._ekeventstore.retainWeakReference(*args, **kwargs)

    def return_event_results(self, *args, **kwargs):
        return self._ekeventstore.returnEventResults(*args, **kwargs)

    def return_reminder_results(self, *args, **kwargs):
        return self._ekeventstore.returnReminderResults(*args, **kwargs)

    def rollback(self, *args, **kwargs):
        return self._ekeventstore.rollback(*args, **kwargs)

    def rollback_objects_with_identifiers_(self, *args, **kwargs):
        return self._ekeventstore.rollbackObjectsWithIdentifiers_(*args, **kwargs)

    def save_attachment_commit_error_(self, *args, **kwargs):
        return self._ekeventstore.saveAttachment_commit_error_(*args, **kwargs)

    def save_calendar_commit_error_(self, *args, **kwargs):
        return self._ekeventstore.saveCalendar_commit_error_(*args, **kwargs)

    def save_calendar_error_(self, *args, **kwargs):
        return self._ekeventstore.saveCalendar_error_(*args, **kwargs)

    def save_draft_of_event_(self, *args, **kwargs):
        return self._ekeventstore.saveDraftOfEvent_(*args, **kwargs)

    def save_event_span_commit_error_(self, *args, **kwargs):
        return self._ekeventstore.saveEvent_span_commit_error_(*args, **kwargs)

    def save_event_span_error_(self, *args, **kwargs):
        return self._ekeventstore.saveEvent_span_error_(*args, **kwargs)

    def save_notification_collection_commit_error_(self, *args, **kwargs):
        return self._ekeventstore.saveNotificationCollection_commit_error_(*args, **kwargs)

    def save_notification_commit_error_(self, *args, **kwargs):
        return self._ekeventstore.saveNotification_commit_error_(*args, **kwargs)

    def save_reminder_commit_error_(self, *args, **kwargs):
        return self._ekeventstore.saveReminder_commit_error_(*args, **kwargs)

    def save_reminder_error_(self, *args, **kwargs):
        return self._ekeventstore.saveReminder_error_(*args, **kwargs)

    def save_source_commit_error_(self, *args, **kwargs):
        return self._ekeventstore.saveSource_commit_error_(*args, **kwargs)

    def save_(self, *args, **kwargs):
        return self._ekeventstore.save_(*args, **kwargs)

    def scripting_properties(self, *args, **kwargs):
        return self._ekeventstore.scriptingProperties(*args, **kwargs)

    def scripting_value_for_specifier_(self, *args, **kwargs):
        return self._ekeventstore.scriptingValueForSpecifier_(*args, **kwargs)

    def self(self, *args, **kwargs):
        return self._ekeventstore.self(*args, **kwargs)

    def sequence_number(self, *args, **kwargs):
        return self._ekeventstore.sequenceNumber(*args, **kwargs)

    def sequence_token(self, *args, **kwargs):
        return self._ekeventstore.sequenceToken(*args, **kwargs)

    def set_accessibility_braille_map_render_region_(self, *args, **kwargs):
        return self._ekeventstore.setAccessibilityBrailleMapRenderRegion_(*args, **kwargs)

    def set_accessibility_braille_map_renderer_(self, *args, **kwargs):
        return self._ekeventstore.setAccessibilityBrailleMapRenderer_(*args, **kwargs)

    def set_birthday_calendar_enabled_(self, *args, **kwargs):
        return self._ekeventstore.setBirthdayCalendarEnabled_(*args, **kwargs)

    def set_birthday_calendar_version_(self, *args, **kwargs):
        return self._ekeventstore.setBirthdayCalendarVersion_(*args, **kwargs)

    def set_cached_default_alarm_offsets_to_n_s_not_found(self, *args, **kwargs):
        return self._ekeventstore.setCachedDefaultAlarmOffsetsToNSNotFound(*args, **kwargs)

    def set_cached_e_k_source_constraint_object_for_key_(self, *args, **kwargs):
        return self._ekeventstore.setCachedEKSourceConstraintObject_forKey_(*args, **kwargs)

    def set_data_protection_observer_(self, *args, **kwargs):
        return self._ekeventstore.setDataProtectionObserver_(*args, **kwargs)

    def set_database_(self, *args, **kwargs):
        return self._ekeventstore.setDatabase_(*args, **kwargs)

    def set_default_calendar_for_new_events_(self, *args, **kwargs):
        return self._ekeventstore.setDefaultCalendarForNewEvents_(*args, **kwargs)

    def set_default_calendar_for_new_events_in_delegate_source_(self, *args, **kwargs):
        return self._ekeventstore.setDefaultCalendar_forNewEventsInDelegateSource_(*args, **kwargs)

    def set_deleted_objects_(self, *args, **kwargs):
        return self._ekeventstore.setDeletedObjects_(*args, **kwargs)

    def set_event_source_id_to_reminder_source_id_mapping_(self, *args, **kwargs):
        return self._ekeventstore.setEventSourceIDToReminderSourceIDMapping_(*args, **kwargs)

    def set_inserted_objects_(self, *args, **kwargs):
        return self._ekeventstore.setInsertedObjects_(*args, **kwargs)

    def set_invitation_status_for_event_error_(self, *args, **kwargs):
        return self._ekeventstore.setInvitationStatus_forEvent_error_(*args, **kwargs)

    def set_invitation_status_for_events_error_(self, *args, **kwargs):
        return self._ekeventstore.setInvitationStatus_forEvents_error_(*args, **kwargs)

    def set_last_database_notification_timestamp_(self, *args, **kwargs):
        return self._ekeventstore.setLastDatabaseNotificationTimestamp_(*args, **kwargs)

    def set_needs_geocoding_for_event_(self, *args, **kwargs):
        return self._ekeventstore.setNeedsGeocoding_forEvent_(*args, **kwargs)

    def set_nil_value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.setNilValueForKey_(*args, **kwargs)

    def set_objects_pending_save_(self, *args, **kwargs):
        return self._ekeventstore.setObjectsPendingSave_(*args, **kwargs)

    def set_observation_info_(self, *args, **kwargs):
        return self._ekeventstore.setObservationInfo_(*args, **kwargs)

    def set_observation_for_observing_key_path_(self, *args, **kwargs):
        return self._ekeventstore.setObservation_forObservingKeyPath_(*args, **kwargs)

    def set_privacy_client_identity_(self, *args, **kwargs):
        return self._ekeventstore.setPrivacyClientIdentity_(*args, **kwargs)

    def set_registered_objects_(self, *args, **kwargs):
        return self._ekeventstore.setRegisteredObjects_(*args, **kwargs)

    def set_reminder_source_id_to_event_source_id_mapping_(self, *args, **kwargs):
        return self._ekeventstore.setReminderSourceIDToEventSourceIDMapping_(*args, **kwargs)

    def set_remote_client_identity_(self, *args, **kwargs):
        return self._ekeventstore.setRemoteClientIdentity_(*args, **kwargs)

    def set_restore_generation_changed_and_get_previous_value_(self, *args, **kwargs):
        return self._ekeventstore.setRestoreGenerationChangedAndGetPreviousValue_(*args, **kwargs)

    def set_restore_generation_changed_(self, *args, **kwargs):
        return self._ekeventstore.setRestoreGenerationChanged_(*args, **kwargs)

    def set_scripting_properties_(self, *args, **kwargs):
        return self._ekeventstore.setScriptingProperties_(*args, **kwargs)

    def set_show_declined_events_(self, *args, **kwargs):
        return self._ekeventstore.setShowDeclinedEvents_(*args, **kwargs)

    def set_skip_modification_validation_(self, *args, **kwargs):
        return self._ekeventstore.setSkipModificationValidation_(*args, **kwargs)

    def set_time_zone_(self, *args, **kwargs):
        return self._ekeventstore.setTimeZone_(*args, **kwargs)

    def set_updated_objects_(self, *args, **kwargs):
        return self._ekeventstore.setUpdatedObjects_(*args, **kwargs)

    def set_user_interface_item_identifier_(self, *args, **kwargs):
        return self._ekeventstore.setUserInterfaceItemIdentifier_(*args, **kwargs)

    def set_value_for_key_path_(self, *args, **kwargs):
        return self._ekeventstore.setValue_forKeyPath_(*args, **kwargs)

    def set_value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.setValue_forKey_(*args, **kwargs)

    def set_value_for_undefined_key_(self, *args, **kwargs):
        return self._ekeventstore.setValue_forUndefinedKey_(*args, **kwargs)

    def set_values_for_keys_with_dictionary_(self, *args, **kwargs):
        return self._ekeventstore.setValuesForKeysWithDictionary_(*args, **kwargs)

    def set_cached_constraints_(self, *args, **kwargs):
        return self._ekeventstore.set_cachedConstraints_(*args, **kwargs)

    def set_cached_default_constraints_(self, *args, **kwargs):
        return self._ekeventstore.set_cachedDefaultConstraints_(*args, **kwargs)

    def set_cached_notification_collections_(self, *args, **kwargs):
        return self._ekeventstore.set_cachedNotificationCollections_(*args, **kwargs)

    def shared_calendar_invitations_for_entity_types_(self, *args, **kwargs):
        return self._ekeventstore.sharedCalendarInvitationsForEntityTypes_(*args, **kwargs)

    def should_permit_organizer_email_from_junk_checks_(self, *args, **kwargs):
        return self._ekeventstore.shouldPermitOrganizerEmailFromJunkChecks_(*args, **kwargs)

    def should_permit_organizer_phone_number_from_junk_checks_(self, *args, **kwargs):
        return self._ekeventstore.shouldPermitOrganizerPhoneNumberFromJunkChecks_(*args, **kwargs)

    def should_record_object_id_map(self, *args, **kwargs):
        return self._ekeventstore.shouldRecordObjectIDMap(*args, **kwargs)

    def should_save_calendar_as_event_calendar_(self, *args, **kwargs):
        return self._ekeventstore.shouldSaveCalendarAsEventCalendar_(*args, **kwargs)

    def should_save_calendar_as_reminder_calendar_(self, *args, **kwargs):
        return self._ekeventstore.shouldSaveCalendarAsReminderCalendar_(*args, **kwargs)

    def show_date_in_calendar_in_view_(self, *args, **kwargs):
        return self._ekeventstore.showDateInCalendar_inView_(*args, **kwargs)

    def show_declined_events(self, *args, **kwargs):
        return self._ekeventstore.showDeclinedEvents(*args, **kwargs)

    def show_declined_events_changed_(self, *args, **kwargs):
        return self._ekeventstore.showDeclinedEventsChanged_(*args, **kwargs)

    def show_event_in_calendar_with_open_options_in_view_(self, *args, **kwargs):
        return self._ekeventstore.showEventInCalendar_withOpenOptions_inView_(*args, **kwargs)

    def siri_suggestions_all_day_alarm_offset(self, *args, **kwargs):
        return self._ekeventstore.siriSuggestionsAllDayAlarmOffset(*args, **kwargs)

    def siri_suggestions_timed_alarm_offset(self, *args, **kwargs):
        return self._ekeventstore.siriSuggestionsTimedAlarmOffset(*args, **kwargs)

    def skip_modification_validation(self, *args, **kwargs):
        return self._ekeventstore.skipModificationValidation(*args, **kwargs)

    def source_identifier_for_event_(self, *args, **kwargs):
        return self._ekeventstore.sourceIdentifierForEvent_(*args, **kwargs)

    def source_with_external_id_(self, *args, **kwargs):
        return self._ekeventstore.sourceWithExternalID_(*args, **kwargs)

    def source_with_identifier_(self, *args, **kwargs):
        return self._ekeventstore.sourceWithIdentifier_(*args, **kwargs)

    def sources(self, *args, **kwargs):
        return self._ekeventstore.sources(*args, **kwargs)

    def sources_enabled_for_entity_type_(self, *args, **kwargs):
        return self._ekeventstore.sourcesEnabledForEntityType_(*args, **kwargs)

    def start_recording_object_id_change_map(self, *args, **kwargs):
        return self._ekeventstore.startRecordingObjectIDChangeMap(*args, **kwargs)

    def stop_recording_object_id_change_map(self, *args, **kwargs):
        return self._ekeventstore.stopRecordingObjectIDChangeMap(*args, **kwargs)

    def stored_value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.storedValueForKey_(*args, **kwargs)

    def string_value_safe(self, *args, **kwargs):
        return self._ekeventstore.stringValueSafe(*args, **kwargs)

    def string_value_safe_(self, *args, **kwargs):
        return self._ekeventstore.stringValueSafe_(*args, **kwargs)

    def suggested_event_calendar(self, *args, **kwargs):
        return self._ekeventstore.suggestedEventCalendar(*args, **kwargs)

    def superclass(self, *args, **kwargs):
        return self._ekeventstore.superclass(*args, **kwargs)

    def supports_b_s_x_p_c_secure_coding(self, *args, **kwargs):
        return self._ekeventstore.supportsBSXPCSecureCoding(*args, **kwargs)

    def supports_r_b_s_x_p_c_secure_coding(self, *args, **kwargs):
        return self._ekeventstore.supportsRBSXPCSecureCoding(*args, **kwargs)

    def sync_error_count(self, *args, **kwargs):
        return self._ekeventstore.syncErrorCount(*args, **kwargs)

    def take_stored_value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.takeStoredValue_forKey_(*args, **kwargs)

    def take_stored_values_from_dictionary_(self, *args, **kwargs):
        return self._ekeventstore.takeStoredValuesFromDictionary_(*args, **kwargs)

    def take_value_for_key_path_(self, *args, **kwargs):
        return self._ekeventstore.takeValue_forKeyPath_(*args, **kwargs)

    def take_value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.takeValue_forKey_(*args, **kwargs)

    def take_values_from_dictionary_(self, *args, **kwargs):
        return self._ekeventstore.takeValuesFromDictionary_(*args, **kwargs)

    def time_to_leave_location_authorization_status(self, *args, **kwargs):
        return self._ekeventstore.timeToLeaveLocationAuthorizationStatus(*args, **kwargs)

    def time_zone(self, *args, **kwargs):
        return self._ekeventstore.timeZone(*args, **kwargs)

    def to_many_relationship_keys(self, *args, **kwargs):
        return self._ekeventstore.toManyRelationshipKeys(*args, **kwargs)

    def to_one_relationship_keys(self, *args, **kwargs):
        return self._ekeventstore.toOneRelationshipKeys(*args, **kwargs)

    def to_p_b_codable(self, *args, **kwargs):
        return self._ekeventstore.toPBCodable(*args, **kwargs)

    def travel_eligible_events_in_calendars_start_date_end_date_(self, *args, **kwargs):
        return self._ekeventstore.travelEligibleEventsInCalendars_startDate_endDate_(*args, **kwargs)

    def un_safe_bool_value(self, *args, **kwargs):
        return self._ekeventstore.un_safeBoolValue(*args, **kwargs)

    def unable_to_set_nil_for_key_(self, *args, **kwargs):
        return self._ekeventstore.unableToSetNilForKey_(*args, **kwargs)

    def unbind_(self, *args, **kwargs):
        return self._ekeventstore.unbind_(*args, **kwargs)

    def unique_identifiers_for_all_objects_with_changes_related_to_objects_(self, *args, **kwargs):
        return self._ekeventstore.uniqueIdentifiersForAllObjectsWithChangesRelatedToObjects_(*args, **kwargs)

    def unique_identifiers_for_events_with_object_ids_(self, *args, **kwargs):
        return self._ekeventstore.uniqueIdentifiersForEventsWithObjectIDs_(*args, **kwargs)

    def unregister_for_detailed_change_tracking_(self, *args, **kwargs):
        return self._ekeventstore.unregisterForDetailedChangeTracking_(*args, **kwargs)

    def unsaved_changes_queue(self, *args, **kwargs):
        return self._ekeventstore.unsavedChangesQueue(*args, **kwargs)

    def update_granted_delegate_action_source_completion_(self, *args, **kwargs):
        return self._ekeventstore.updateGrantedDelegate_action_source_completion_(*args, **kwargs)

    def updated_object_ids(self, *args, **kwargs):
        return self._ekeventstore.updatedObjectIDs(*args, **kwargs)

    def updated_objects(self, *args, **kwargs):
        return self._ekeventstore.updatedObjects(*args, **kwargs)

    def user_interface_item_identifier(self, *args, **kwargs):
        return self._ekeventstore.userInterfaceItemIdentifier(*args, **kwargs)

    def utf8_value_safe(self, *args, **kwargs):
        return self._ekeventstore.utf8ValueSafe(*args, **kwargs)

    def utf8_value_safe_(self, *args, **kwargs):
        return self._ekeventstore.utf8ValueSafe_(*args, **kwargs)

    def validate_take_value_for_key_path_(self, *args, **kwargs):
        return self._ekeventstore.validateTakeValue_forKeyPath_(*args, **kwargs)

    def validate_value_for_key_path_error_(self, *args, **kwargs):
        return self._ekeventstore.validateValue_forKeyPath_error_(*args, **kwargs)

    def validate_value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.validateValue_forKey_(*args, **kwargs)

    def validate_value_for_key_error_(self, *args, **kwargs):
        return self._ekeventstore.validateValue_forKey_error_(*args, **kwargs)

    def validated_non_deleted_persistent_object_with_object_id_(self, *args, **kwargs):
        return self._ekeventstore.validatedNonDeletedPersistentObjectWithObjectID_(*args, **kwargs)

    def validated_non_deleted_public_object_with_object_id_(self, *args, **kwargs):
        return self._ekeventstore.validatedNonDeletedPublicObjectWithObjectID_(*args, **kwargs)

    def value_at_index_in_property_with_key_(self, *args, **kwargs):
        return self._ekeventstore.valueAtIndex_inPropertyWithKey_(*args, **kwargs)

    def value_class_for_binding_(self, *args, **kwargs):
        return self._ekeventstore.valueClassForBinding_(*args, **kwargs)

    def value_for_key_path_(self, *args, **kwargs):
        return self._ekeventstore.valueForKeyPath_(*args, **kwargs)

    def value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.valueForKey_(*args, **kwargs)

    def value_for_undefined_key_(self, *args, **kwargs):
        return self._ekeventstore.valueForUndefinedKey_(*args, **kwargs)

    def value_with_name_in_property_with_key_(self, *args, **kwargs):
        return self._ekeventstore.valueWithName_inPropertyWithKey_(*args, **kwargs)

    def value_with_unique_id_in_property_with_key_(self, *args, **kwargs):
        return self._ekeventstore.valueWithUniqueID_inPropertyWithKey_(*args, **kwargs)

    def values_for_keys_(self, *args, **kwargs):
        return self._ekeventstore.valuesForKeys_(*args, **kwargs)

    def wait_until_database_updated_to_timestamp_callback_(self, *args, **kwargs):
        return self._ekeventstore.waitUntilDatabaseUpdatedToTimestamp_callback_(*args, **kwargs)

    def will_change_value_for_key_(self, *args, **kwargs):
        return self._ekeventstore.willChangeValueForKey_(*args, **kwargs)

    def will_change_value_for_key_with_set_mutation_using_objects_(self, *args, **kwargs):
        return self._ekeventstore.willChangeValueForKey_withSetMutation_usingObjects_(*args, **kwargs)

    def will_change_values_at_indexes_for_key_(self, *args, **kwargs):
        return self._ekeventstore.willChange_valuesAtIndexes_forKey_(*args, **kwargs)

    def zone(self, *args, **kwargs):
        return self._ekeventstore.zone(*args, **kwargs)


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()
    store = EKEventStoreWrapper()
    print(store.zone())


if __name__ == '__main__':
    main()
