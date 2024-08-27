
class EKEventWrapper:
    def __init__(self):
        import EventKit

        self._ekevent = EventKit.EKEvent.alloc().init()

    def c_a_d_object_i_d(self, *args, **kwargs):
        return self._ekevent.CADObjectID(*args, **kwargs)
    
    def c_a_m_l_type(self, *args, **kwargs):
        return self._ekevent.CAMLType(*args, **kwargs)
    
    def c_a_m_l_type_for_key_(self, *args, **kwargs):
        return self._ekevent.CAMLTypeForKey_(*args, **kwargs)
    
    def c_a_m_l_type_supported_for_key_(self, *args, **kwargs):
        return self._ekevent.CAMLTypeSupportedForKey_(*args, **kwargs)
    
    def c_a_add_value_multiplied_by_(self, *args, **kwargs):
        return self._ekevent.CA_addValue_multipliedBy_(*args, **kwargs)
    
    def c_a_archiving_value_for_key_(self, *args, **kwargs):
        return self._ekevent.CA_archivingValueForKey_(*args, **kwargs)
    
    def c_a_copy_numeric_value_(self, *args, **kwargs):
        return self._ekevent.CA_copyNumericValue_(*args, **kwargs)
    
    def c_a_copy_render_value(self, *args, **kwargs):
        return self._ekevent.CA_copyRenderValue(*args, **kwargs)
    
    def c_a_copy_render_value_with_colorspace_(self, *args, **kwargs):
        return self._ekevent.CA_copyRenderValueWithColorspace_(*args, **kwargs)
    
    def c_a_distance_to_value_(self, *args, **kwargs):
        return self._ekevent.CA_distanceToValue_(*args, **kwargs)
    
    def c_a_interpolate_value_by_fraction_(self, *args, **kwargs):
        return self._ekevent.CA_interpolateValue_byFraction_(*args, **kwargs)
    
    def c_a_interpolate_values___interpolator_(self, *args, **kwargs):
        return self._ekevent.CA_interpolateValues___interpolator_(*args, **kwargs)
    
    def c_a_numeric_value_count(self, *args, **kwargs):
        return self._ekevent.CA_numericValueCount(*args, **kwargs)
    
    def c_a_prepare_render_value(self, *args, **kwargs):
        return self._ekevent.CA_prepareRenderValue(*args, **kwargs)
    
    def c_a_round_to_integer_from_value_(self, *args, **kwargs):
        return self._ekevent.CA_roundToIntegerFromValue_(*args, **kwargs)
    
    def c_a_validate_value_for_key_(self, *args, **kwargs):
        return self._ekevent.CA_validateValue_forKey_(*args, **kwargs)
    
    def c_k_assign_to_container_with_i_d_(self, *args, **kwargs):
        return self._ekevent.CKAssignToContainerWithID_(*args, **kwargs)
    
    def c_k_description(self, *args, **kwargs):
        return self._ekevent.CKDescription(*args, **kwargs)
    
    def c_k_description_class_name(self, *args, **kwargs):
        return self._ekevent.CKDescriptionClassName(*args, **kwargs)
    
    def c_k_description_properties_with_public_private_should_expand_(self, *args, **kwargs):
        return self._ekevent.CKDescriptionPropertiesWithPublic_private_shouldExpand_(*args, **kwargs)
    
    def c_k_description_redact_avoid_short_description_(self, *args, **kwargs):
        return self._ekevent.CKDescriptionRedact_avoidShortDescription_(*args, **kwargs)
    
    def c_k_description_should_print_pointer(self, *args, **kwargs):
        return self._ekevent.CKDescriptionShouldPrintPointer(*args, **kwargs)
    
    def c_k_expanded_description(self, *args, **kwargs):
        return self._ekevent.CKExpandedDescription(*args, **kwargs)
    
    def c_k_object_description_redact_(self, *args, **kwargs):
        return self._ekevent.CKObjectDescriptionRedact_(*args, **kwargs)
    
    def c_k_object_description_redact_avoid_short_description_(self, *args, **kwargs):
        return self._ekevent.CKObjectDescriptionRedact_avoidShortDescription_(*args, **kwargs)
    
    def c_k_properties_description(self, *args, **kwargs):
        return self._ekevent.CKPropertiesDescription(*args, **kwargs)
    
    def c_k_redacted_description(self, *args, **kwargs):
        return self._ekevent.CKRedactedDescription(*args, **kwargs)
    
    def c_k_unredacted_description(self, *args, **kwargs):
        return self._ekevent.CKUnredactedDescription(*args, **kwargs)
    
    def cal_class_name(self, *args, **kwargs):
        return self._ekevent.CalClassName(*args, **kwargs)
    
    def n_s_lifeguard_autorelease(self, *args, **kwargs):
        return self._ekevent.NSLifeguard_autorelease(*args, **kwargs)
    
    def n_s_representation(self, *args, **kwargs):
        return self._ekevent.NSRepresentation(*args, **kwargs)
    
    def n_s_representation(self, *args, **kwargs):
        return self._ekevent.NSRepresentation(*args, **kwargs)
    
    def n_s_observation_for_key_path_options_block_(self, *args, **kwargs):
        return self._ekevent.NS_observationForKeyPath_options_block_(*args, **kwargs)
    
    def n_s_observation_for_key_paths_options_block_(self, *args, **kwargs):
        return self._ekevent.NS_observationForKeyPaths_options_block_(*args, **kwargs)
    
    def r_b_s_is_x_p_c_object(self, *args, **kwargs):
        return self._ekevent.RBSIsXPCObject(*args, **kwargs)
    
    def s_c_n_u_i_name(self, *args, **kwargs):
        return self._ekevent.SCNUI_name(*args, **kwargs)
    
    def s_c_n_setup_display_link_with_queue_screen_policy_(self, *args, **kwargs):
        return self._ekevent.SCN_setupDisplayLinkWithQueue_screen_policy_(*args, **kwargs)
    
    def u_r_l(self, *args, **kwargs):
        return self._ekevent.URL(*args, **kwargs)
    
    def u_r_l(self, *args, **kwargs):
        return self._ekevent.URL(*args, **kwargs)
    
    def u_r_l_string(self, *args, **kwargs):
        return self._ekevent.URLString(*args, **kwargs)
    
    def u_u_i_d(self, *args, **kwargs):
        return self._ekevent.UUID(*args, **kwargs)
    
    def v_n_compute_device_performance_score(self, *args, **kwargs):
        return self._ekevent.VNComputeDevicePerformanceScore(*args, **kwargs)
    
    def v_n_compute_device_type(self, *args, **kwargs):
        return self._ekevent.VNComputeDeviceType(*args, **kwargs)
    
    def ab_case_insensitive_is_equal_(self, *args, **kwargs):
        return self._ekevent.abCaseInsensitiveIsEqual_(*args, **kwargs)
    
    def ab_dictionary_with_values_for_key_paths_(self, *args, **kwargs):
        return self._ekevent.abDictionaryWithValuesForKeyPaths_(*args, **kwargs)
    
    def ab_remove_observer_ignoring_exceptions_for_key_path_(self, *args, **kwargs):
        return self._ekevent.abRemoveObserverIgnoringExceptions_forKeyPath_(*args, **kwargs)
    
    def accept_proposed_time_notification_from_attendee_(self, *args, **kwargs):
        return self._ekevent.acceptProposedTimeNotificationFromAttendee_(*args, **kwargs)
    
    def accessibility_add_temporary_child_(self, *args, **kwargs):
        return self._ekevent.accessibilityAddTemporaryChild_(*args, **kwargs)
    
    def accessibility_allows_overridden_attributes_when_ignored(self, *args, **kwargs):
        return self._ekevent.accessibilityAllowsOverriddenAttributesWhenIgnored(*args, **kwargs)
    
    def accessibility_array_attribute_count_(self, *args, **kwargs):
        return self._ekevent.accessibilityArrayAttributeCount_(*args, **kwargs)
    
    def accessibility_array_attribute_values_index_max_count_(self, *args, **kwargs):
        return self._ekevent.accessibilityArrayAttributeValues_index_maxCount_(*args, **kwargs)
    
    def accessibility_attribute_value_for_parameter_(self, *args, **kwargs):
        return self._ekevent.accessibilityAttributeValue_forParameter_(*args, **kwargs)
    
    def accessibility_attributed_value_for_string_attribute_attribute_for_parameter_(self, *args, **kwargs):
        return self._ekevent.accessibilityAttributedValueForStringAttributeAttributeForParameter_(*args, **kwargs)
    
    def accessibility_braille_map_render_region(self, *args, **kwargs):
        return self._ekevent.accessibilityBrailleMapRenderRegion(*args, **kwargs)
    
    def accessibility_braille_map_renderer(self, *args, **kwargs):
        return self._ekevent.accessibilityBrailleMapRenderer(*args, **kwargs)
    
    def accessibility_decode_overridden_attributes_(self, *args, **kwargs):
        return self._ekevent.accessibilityDecodeOverriddenAttributes_(*args, **kwargs)
    
    def accessibility_encode_overridden_attributes_(self, *args, **kwargs):
        return self._ekevent.accessibilityEncodeOverriddenAttributes_(*args, **kwargs)
    
    def accessibility_index_for_child_u_i_element_attribute_for_parameter_(self, *args, **kwargs):
        return self._ekevent.accessibilityIndexForChildUIElementAttributeForParameter_(*args, **kwargs)
    
    def accessibility_index_of_child_(self, *args, **kwargs):
        return self._ekevent.accessibilityIndexOfChild_(*args, **kwargs)
    
    def accessibility_overridden_attributes(self, *args, **kwargs):
        return self._ekevent.accessibilityOverriddenAttributes(*args, **kwargs)
    
    def accessibility_parameterized_attribute_names(self, *args, **kwargs):
        return self._ekevent.accessibilityParameterizedAttributeNames(*args, **kwargs)
    
    def accessibility_perform_show_menu_of_child_(self, *args, **kwargs):
        return self._ekevent.accessibilityPerformShowMenuOfChild_(*args, **kwargs)
    
    def accessibility_presenter_process_identifier(self, *args, **kwargs):
        return self._ekevent.accessibilityPresenterProcessIdentifier(*args, **kwargs)
    
    def accessibility_remove_temporary_child_(self, *args, **kwargs):
        return self._ekevent.accessibilityRemoveTemporaryChild_(*args, **kwargs)
    
    def accessibility_replace_range_with_text_(self, *args, **kwargs):
        return self._ekevent.accessibilityReplaceRange_withText_(*args, **kwargs)
    
    def accessibility_set_override_value_for_attribute_(self, *args, **kwargs):
        return self._ekevent.accessibilitySetOverrideValue_forAttribute_(*args, **kwargs)
    
    def accessibility_set_presenter_process_identifier_(self, *args, **kwargs):
        return self._ekevent.accessibilitySetPresenterProcessIdentifier_(*args, **kwargs)
    
    def accessibility_should_send_notification_(self, *args, **kwargs):
        return self._ekevent.accessibilityShouldSendNotification_(*args, **kwargs)
    
    def accessibility_should_use_unique_id(self, *args, **kwargs):
        return self._ekevent.accessibilityShouldUseUniqueId(*args, **kwargs)
    
    def accessibility_supports_custom_element_data(self, *args, **kwargs):
        return self._ekevent.accessibilitySupportsCustomElementData(*args, **kwargs)
    
    def accessibility_supports_notifications(self, *args, **kwargs):
        return self._ekevent.accessibilitySupportsNotifications(*args, **kwargs)
    
    def accessibility_supports_overridden_attributes(self, *args, **kwargs):
        return self._ekevent.accessibilitySupportsOverriddenAttributes(*args, **kwargs)
    
    def accessibility_temporary_children(self, *args, **kwargs):
        return self._ekevent.accessibilityTemporaryChildren(*args, **kwargs)
    
    def accessibility_visible_area(self, *args, **kwargs):
        return self._ekevent.accessibilityVisibleArea(*args, **kwargs)
    
    def action(self, *args, **kwargs):
        return self._ekevent.action(*args, **kwargs)
    
    def action_string(self, *args, **kwargs):
        return self._ekevent.actionString(*args, **kwargs)
    
    def actions(self, *args, **kwargs):
        return self._ekevent.actions(*args, **kwargs)
    
    def actions_state(self, *args, **kwargs):
        return self._ekevent.actionsState(*args, **kwargs)
    
    def add_alarm_(self, *args, **kwargs):
        return self._ekevent.addAlarm_(*args, **kwargs)
    
    def add_attachment_(self, *args, **kwargs):
        return self._ekevent.addAttachment_(*args, **kwargs)
    
    def add_attendee_(self, *args, **kwargs):
        return self._ekevent.addAttendee_(*args, **kwargs)
    
    def add_cached_melted_object_for_multi_value_key_(self, *args, **kwargs):
        return self._ekevent.addCachedMeltedObject_forMultiValueKey_(*args, **kwargs)
    
    def add_chained_observers_(self, *args, **kwargs):
        return self._ekevent.addChainedObservers_(*args, **kwargs)
    
    def add_changes_from_object_(self, *args, **kwargs):
        return self._ekevent.addChangesFromObject_(*args, **kwargs)
    
    def add_changes_from_object_copying_backing_objects_(self, *args, **kwargs):
        return self._ekevent.addChangesFromObject_copyingBackingObjects_(*args, **kwargs)
    
    def add_changes_(self, *args, **kwargs):
        return self._ekevent.addChanges_(*args, **kwargs)
    
    def add_co_commit_object_(self, *args, **kwargs):
        return self._ekevent.addCoCommitObject_(*args, **kwargs)
    
    def add_conference_rooms_(self, *args, **kwargs):
        return self._ekevent.addConferenceRooms_(*args, **kwargs)
    
    def add_event_action_(self, *args, **kwargs):
        return self._ekevent.addEventAction_(*args, **kwargs)
    
    def add_multi_changed_object_value_for_key_(self, *args, **kwargs):
        return self._ekevent.addMultiChangedObjectValue_forKey_(*args, **kwargs)
    
    def add_multi_changed_object_values_for_key_(self, *args, **kwargs):
        return self._ekevent.addMultiChangedObjectValues_forKey_(*args, **kwargs)
    
    def add_object_to_both_sides_of_relationship_with_key_(self, *args, **kwargs):
        return self._ekevent.addObject_toBothSidesOfRelationshipWithKey_(*args, **kwargs)
    
    def add_object_to_property_with_key_(self, *args, **kwargs):
        return self._ekevent.addObject_toPropertyWithKey_(*args, **kwargs)
    
    def add_observation_transformer_(self, *args, **kwargs):
        return self._ekevent.addObservationTransformer_(*args, **kwargs)
    
    def add_observer_block_(self, *args, **kwargs):
        return self._ekevent.addObserverBlock_(*args, **kwargs)
    
    def add_observer_(self, *args, **kwargs):
        return self._ekevent.addObserver_(*args, **kwargs)
    
    def add_observer_for_key_path_options_context_(self, *args, **kwargs):
        return self._ekevent.addObserver_forKeyPath_options_context_(*args, **kwargs)
    
    def add_observer_for_observable_key_path_(self, *args, **kwargs):
        return self._ekevent.addObserver_forObservableKeyPath_(*args, **kwargs)
    
    def add_organizer_and_self_attendee_for_new_invitation(self, *args, **kwargs):
        return self._ekevent.addOrganizerAndSelfAttendeeForNewInvitation(*args, **kwargs)
    
    def add_recurrence_rule_(self, *args, **kwargs):
        return self._ekevent.addRecurrenceRule_(*args, **kwargs)
    
    def additional_frozen_properties(self, *args, **kwargs):
        return self._ekevent.additionalFrozenProperties(*args, **kwargs)
    
    def additional_melted_objects(self, *args, **kwargs):
        return self._ekevent.additionalMeltedObjects(*args, **kwargs)
    
    def adjust_date_from_u_t_c_(self, *args, **kwargs):
        return self._ekevent.adjustDateFromUTC_(*args, **kwargs)
    
    def adjusted_persisted_date_for_date_persisted_date_is_in_u_t_c_with_adjustment_mode_pin_mode_client_calendar_date_(self, *args, **kwargs):
        return self._ekevent.adjustedPersistedDateForDate_persistedDateIsInUTC_withAdjustmentMode_pinMode_clientCalendarDate_(*args, **kwargs)
    
    def adjusted_persisted_date_for_date_with_adjustment_mode_pin_mode_client_calendar_date_(self, *args, **kwargs):
        return self._ekevent.adjustedPersistedDateForDate_withAdjustmentMode_pinMode_clientCalendarDate_(*args, **kwargs)
    
    def alarms(self, *args, **kwargs):
        return self._ekevent.alarms(*args, **kwargs)
    
    def all_alarms(self, *args, **kwargs):
        return self._ekevent.allAlarms(*args, **kwargs)
    
    def all_alarms_set(self, *args, **kwargs):
        return self._ekevent.allAlarmsSet(*args, **kwargs)
    
    def all_property_keys(self, *args, **kwargs):
        return self._ekevent.allPropertyKeys(*args, **kwargs)
    
    def allows_alarm_modifications(self, *args, **kwargs):
        return self._ekevent.allowsAlarmModifications(*args, **kwargs)
    
    def allows_alarm_modifications(self, *args, **kwargs):
        return self._ekevent.allowsAlarmModifications(*args, **kwargs)
    
    def allows_all_day_modifications(self, *args, **kwargs):
        return self._ekevent.allowsAllDayModifications(*args, **kwargs)
    
    def allows_attendees_modifications(self, *args, **kwargs):
        return self._ekevent.allowsAttendeesModifications(*args, **kwargs)
    
    def allows_attendees_modifications(self, *args, **kwargs):
        return self._ekevent.allowsAttendeesModifications(*args, **kwargs)
    
    def allows_availability_modifications(self, *args, **kwargs):
        return self._ekevent.allowsAvailabilityModifications(*args, **kwargs)
    
    def allows_calendar_modifications(self, *args, **kwargs):
        return self._ekevent.allowsCalendarModifications(*args, **kwargs)
    
    def allows_calendar_modifications(self, *args, **kwargs):
        return self._ekevent.allowsCalendarModifications(*args, **kwargs)
    
    def allows_participation_status_modifications(self, *args, **kwargs):
        return self._ekevent.allowsParticipationStatusModifications(*args, **kwargs)
    
    def allows_privacy_level_modifications(self, *args, **kwargs):
        return self._ekevent.allowsPrivacyLevelModifications(*args, **kwargs)
    
    def allows_proposed_time_modifications(self, *args, **kwargs):
        return self._ekevent.allowsProposedTimeModifications(*args, **kwargs)
    
    def allows_recurrence_modifications(self, *args, **kwargs):
        return self._ekevent.allowsRecurrenceModifications(*args, **kwargs)
    
    def allows_recurrence_modifications(self, *args, **kwargs):
        return self._ekevent.allowsRecurrenceModifications(*args, **kwargs)
    
    def allows_response_comment_modifications(self, *args, **kwargs):
        return self._ekevent.allowsResponseCommentModifications(*args, **kwargs)
    
    def allows_spans_other_than_this_event(self, *args, **kwargs):
        return self._ekevent.allowsSpansOtherThanThisEvent(*args, **kwargs)
    
    def allows_spans_other_than_this_event(self, *args, **kwargs):
        return self._ekevent.allowsSpansOtherThanThisEvent(*args, **kwargs)
    
    def allows_travel_time_modifications(self, *args, **kwargs):
        return self._ekevent.allowsTravelTimeModifications(*args, **kwargs)
    
    def allows_weak_reference(self, *args, **kwargs):
        return self._ekevent.allowsWeakReference(*args, **kwargs)
    
    def app_link(self, *args, **kwargs):
        return self._ekevent.appLink(*args, **kwargs)
    
    def apply_changes_(self, *args, **kwargs):
        return self._ekevent.applyChanges_(*args, **kwargs)
    
    def attachments(self, *args, **kwargs):
        return self._ekevent.attachments(*args, **kwargs)
    
    def attachments_set(self, *args, **kwargs):
        return self._ekevent.attachmentsSet(*args, **kwargs)
    
    def attendee_comment(self, *args, **kwargs):
        return self._ekevent.attendeeComment(*args, **kwargs)
    
    def attendee_declined_start_date(self, *args, **kwargs):
        return self._ekevent.attendeeDeclinedStartDate(*args, **kwargs)
    
    def attendee_for_me(self, *args, **kwargs):
        return self._ekevent.attendeeForMe(*args, **kwargs)
    
    def attendee_matching_email_address_(self, *args, **kwargs):
        return self._ekevent.attendeeMatchingEmailAddress_(*args, **kwargs)
    
    def attendee_proposed_start_date(self, *args, **kwargs):
        return self._ekevent.attendeeProposedStartDate(*args, **kwargs)
    
    def attendee_reply_changed(self, *args, **kwargs):
        return self._ekevent.attendeeReplyChanged(*args, **kwargs)
    
    def attendee_status(self, *args, **kwargs):
        return self._ekevent.attendeeStatus(*args, **kwargs)
    
    def attendees(self, *args, **kwargs):
        return self._ekevent.attendees(*args, **kwargs)
    
    def attendees_not_including_organizer(self, *args, **kwargs):
        return self._ekevent.attendeesNotIncludingOrganizer(*args, **kwargs)
    
    def attendees_raw(self, *args, **kwargs):
        return self._ekevent.attendeesRaw(*args, **kwargs)
    
    def attribute_keys(self, *args, **kwargs):
        return self._ekevent.attributeKeys(*args, **kwargs)
    
    def augment_melted_object_cache_(self, *args, **kwargs):
        return self._ekevent.augmentMeltedObjectCache_(*args, **kwargs)
    
    def auto_content_accessing_proxy(self, *args, **kwargs):
        return self._ekevent.autoContentAccessingProxy(*args, **kwargs)
    
    def automatic_location_geocoding_allowed(self, *args, **kwargs):
        return self._ekevent.automaticLocationGeocodingAllowed(*args, **kwargs)
    
    def autorelease(self, *args, **kwargs):
        return self._ekevent.autorelease(*args, **kwargs)
    
    def availability(self, *args, **kwargs):
        return self._ekevent.availability(*args, **kwargs)
    
    def awake_after_using_coder_(self, *args, **kwargs):
        return self._ekevent.awakeAfterUsingCoder_(*args, **kwargs)
    
    def awake_from_nib(self, *args, **kwargs):
        return self._ekevent.awakeFromNib(*args, **kwargs)
    
    def backing_object(self, *args, **kwargs):
        return self._ekevent.backingObject(*args, **kwargs)
    
    def backing_object_of_child_object_with_relationship_key_(self, *args, **kwargs):
        return self._ekevent.backingObjectOfChildObject_withRelationshipKey_(*args, **kwargs)
    
    def bind_to_object_with_key_path_options_(self, *args, **kwargs):
        return self._ekevent.bind_toObject_withKeyPath_options_(*args, **kwargs)
    
    def birthday_contact_identifier(self, *args, **kwargs):
        return self._ekevent.birthdayContactIdentifier(*args, **kwargs)
    
    def birthday_contact_name(self, *args, **kwargs):
        return self._ekevent.birthdayContactName(*args, **kwargs)
    
    def birthday_i_d(self, *args, **kwargs):
        return self._ekevent.birthdayID(*args, **kwargs)
    
    def birthday_person_i_d(self, *args, **kwargs):
        return self._ekevent.birthdayPersonID(*args, **kwargs)
    
    def birthday_person_unique_i_d(self, *args, **kwargs):
        return self._ekevent.birthdayPersonUniqueID(*args, **kwargs)
    
    def bool_value_safe(self, *args, **kwargs):
        return self._ekevent.boolValueSafe(*args, **kwargs)
    
    def bool_value_safe_(self, *args, **kwargs):
        return self._ekevent.boolValueSafe_(*args, **kwargs)
    
    def bs_is_plistable_type(self, *args, **kwargs):
        return self._ekevent.bs_isPlistableType(*args, **kwargs)
    
    def bs_secure_encoded(self, *args, **kwargs):
        return self._ekevent.bs_secureEncoded(*args, **kwargs)
    
    def cached_junk_status(self, *args, **kwargs):
        return self._ekevent.cachedJunkStatus(*args, **kwargs)
    
    def cached_melted_child_identifier_to_parent_map(self, *args, **kwargs):
        return self._ekevent.cachedMeltedChildIdentifierToParentMap(*args, **kwargs)
    
    def cached_melted_object_for_single_value_key_(self, *args, **kwargs):
        return self._ekevent.cachedMeltedObjectForSingleValueKey_(*args, **kwargs)
    
    def cached_melted_objects(self, *args, **kwargs):
        return self._ekevent.cachedMeltedObjects(*args, **kwargs)
    
    def cached_melted_objects(self, *args, **kwargs):
        return self._ekevent.cachedMeltedObjects(*args, **kwargs)
    
    def cached_melted_objects_for_multi_value_key_(self, *args, **kwargs):
        return self._ekevent.cachedMeltedObjectsForMultiValueKey_(*args, **kwargs)
    
    def cached_value_for_key_(self, *args, **kwargs):
        return self._ekevent.cachedValueForKey_(*args, **kwargs)
    
    def cached_value_for_key_expecting_cached_value_for_master_key_related_keys_populate_block_(self, *args, **kwargs):
        return self._ekevent.cachedValueForKey_expectingCachedValue_forMasterKey_relatedKeys_populateBlock_(*args, **kwargs)
    
    def cached_value_for_key_populate_block_(self, *args, **kwargs):
        return self._ekevent.cachedValueForKey_populateBlock_(*args, **kwargs)
    
    def calendar(self, *args, **kwargs):
        return self._ekevent.calendar(*args, **kwargs)
    
    def calendar_item_external_identifier(self, *args, **kwargs):
        return self._ekevent.calendarItemExternalIdentifier(*args, **kwargs)
    
    def calendar_item_identifier(self, *args, **kwargs):
        return self._ekevent.calendarItemIdentifier(*args, **kwargs)
    
    def calendar_scale(self, *args, **kwargs):
        return self._ekevent.calendarScale(*args, **kwargs)
    
    def can_be_converted_to_full_object(self, *args, **kwargs):
        return self._ekevent.canBeConvertedToFullObject(*args, **kwargs)
    
    def can_be_responded_to(self, *args, **kwargs):
        return self._ekevent.canBeRespondedTo(*args, **kwargs)
    
    def can_detach_single_occurrence(self, *args, **kwargs):
        return self._ekevent.canDetachSingleOccurrence(*args, **kwargs)
    
    def can_forward(self, *args, **kwargs):
        return self._ekevent.canForward(*args, **kwargs)
    
    def can_move_or_copy_to_calendar_from_calendar_error_(self, *args, **kwargs):
        return self._ekevent.canMoveOrCopyToCalendar_fromCalendar_error_(*args, **kwargs)
    
    def can_move_or_copy_to_calendar_from_calendar_error_(self, *args, **kwargs):
        return self._ekevent.canMoveOrCopyToCalendar_fromCalendar_error_(*args, **kwargs)
    
    def can_move_to_calendar_error_(self, *args, **kwargs):
        return self._ekevent.canMoveToCalendar_error_(*args, **kwargs)
    
    def can_move_to_calendar_from_calendar_allowed_requirements_error_(self, *args, **kwargs):
        return self._ekevent.canMoveToCalendar_fromCalendar_allowedRequirements_error_(*args, **kwargs)
    
    def can_move_to_calendar_from_calendar_error_(self, *args, **kwargs):
        return self._ekevent.canMoveToCalendar_fromCalendar_error_(*args, **kwargs)
    
    def can_move_to_calendar_from_calendar_error_(self, *args, **kwargs):
        return self._ekevent.canMoveToCalendar_fromCalendar_error_(*args, **kwargs)
    
    def change_set(self, *args, **kwargs):
        return self._ekevent.changeSet(*args, **kwargs)
    
    def changed_keys(self, *args, **kwargs):
        return self._ekevent.changedKeys(*args, **kwargs)
    
    def changing_all_day_property_is_allowed(self, *args, **kwargs):
        return self._ekevent.changingAllDayPropertyIsAllowed(*args, **kwargs)
    
    def ck_bind_in_statement_at_index_(self, *args, **kwargs):
        return self._ekevent.ck_bindInStatement_atIndex_(*args, **kwargs)
    
    def cksqlcs_append_s_q_l_constant_value_to_string_(self, *args, **kwargs):
        return self._ekevent.cksqlcs_appendSQLConstantValueToString_(*args, **kwargs)
    
    def cksqlcs_archived_object_binding_value_(self, *args, **kwargs):
        return self._ekevent.cksqlcs_archivedObjectBindingValue_(*args, **kwargs)
    
    def cksqlcs_bind_archived_object_index_db_(self, *args, **kwargs):
        return self._ekevent.cksqlcs_bindArchivedObject_index_db_(*args, **kwargs)
    
    def cksqlcs_bind_blob_index_db_(self, *args, **kwargs):
        return self._ekevent.cksqlcs_bindBlob_index_db_(*args, **kwargs)
    
    def cksqlcs_bind_double_index_db_(self, *args, **kwargs):
        return self._ekevent.cksqlcs_bindDouble_index_db_(*args, **kwargs)
    
    def cksqlcs_bind_int64_index_db_(self, *args, **kwargs):
        return self._ekevent.cksqlcs_bindInt64_index_db_(*args, **kwargs)
    
    def cksqlcs_bind_text_index_db_(self, *args, **kwargs):
        return self._ekevent.cksqlcs_bindText_index_db_(*args, **kwargs)
    
    def cksqlcs_blob_binding_value_destructor_error_(self, *args, **kwargs):
        return self._ekevent.cksqlcs_blobBindingValue_destructor_error_(*args, **kwargs)
    
    def cksqlcs_double_binding_value_(self, *args, **kwargs):
        return self._ekevent.cksqlcs_doubleBindingValue_(*args, **kwargs)
    
    def cksqlcs_int64_binding_value_(self, *args, **kwargs):
        return self._ekevent.cksqlcs_int64BindingValue_(*args, **kwargs)
    
    def cksqlcs_text_binding_value_destructor_error_(self, *args, **kwargs):
        return self._ekevent.cksqlcs_textBindingValue_destructor_error_(*args, **kwargs)
    
    def class_code(self, *args, **kwargs):
        return self._ekevent.classCode(*args, **kwargs)
    
    def class_description(self, *args, **kwargs):
        return self._ekevent.classDescription(*args, **kwargs)
    
    def class_description_for_destination_key_(self, *args, **kwargs):
        return self._ekevent.classDescriptionForDestinationKey_(*args, **kwargs)
    
    def class_for_archiver(self, *args, **kwargs):
        return self._ekevent.classForArchiver(*args, **kwargs)
    
    def class_for_coder(self, *args, **kwargs):
        return self._ekevent.classForCoder(*args, **kwargs)
    
    def class_for_keyed_archiver(self, *args, **kwargs):
        return self._ekevent.classForKeyedArchiver(*args, **kwargs)
    
    def class_for_port_coder(self, *args, **kwargs):
        return self._ekevent.classForPortCoder(*args, **kwargs)
    
    def class_name(self, *args, **kwargs):
        return self._ekevent.className(*args, **kwargs)
    
    def class__(self, *args, **kwargs):
        return self._ekevent.class__(*args, **kwargs)
    
    def clear_cached_time_values(self, *args, **kwargs):
        return self._ekevent.clearCachedTimeValues(*args, **kwargs)
    
    def clear_cached_value_for_key_(self, *args, **kwargs):
        return self._ekevent.clearCachedValueForKey_(*args, **kwargs)
    
    def clear_cached_values_for_keys_(self, *args, **kwargs):
        return self._ekevent.clearCachedValuesForKeys_(*args, **kwargs)
    
    def clear_detected_conference_u_r_l(self, *args, **kwargs):
        return self._ekevent.clearDetectedConferenceURL(*args, **kwargs)
    
    def clear_invitation_status(self, *args, **kwargs):
        return self._ekevent.clearInvitationStatus(*args, **kwargs)
    
    def clear_modified_flags(self, *args, **kwargs):
        return self._ekevent.clearModifiedFlags(*args, **kwargs)
    
    def clear_parsed_conference(self, *args, **kwargs):
        return self._ekevent.clearParsedConference(*args, **kwargs)
    
    def clear_properties(self, *args, **kwargs):
        return self._ekevent.clearProperties(*args, **kwargs)
    
    def clear_virtual_conference_u_r_ls_queued_for_invalidation(self, *args, **kwargs):
        return self._ekevent.clearVirtualConferenceURLsQueuedForInvalidation(*args, **kwargs)
    
    def client_location(self, *args, **kwargs):
        return self._ekevent.clientLocation(*args, **kwargs)
    
    def coerce_value_for_scripting_properties_(self, *args, **kwargs):
        return self._ekevent.coerceValueForScriptingProperties_(*args, **kwargs)
    
    def coerce_value_for_key_(self, *args, **kwargs):
        return self._ekevent.coerceValue_forKey_(*args, **kwargs)
    
    def committed_constraints(self, *args, **kwargs):
        return self._ekevent.committedConstraints(*args, **kwargs)
    
    def committed_constraints(self, *args, **kwargs):
        return self._ekevent.committedConstraints(*args, **kwargs)
    
    def committed_copy(self, *args, **kwargs):
        return self._ekevent.committedCopy(*args, **kwargs)
    
    def committed_copy(self, *args, **kwargs):
        return self._ekevent.committedCopy(*args, **kwargs)
    
    def committed_value_for_key_(self, *args, **kwargs):
        return self._ekevent.committedValueForKey_(*args, **kwargs)
    
    def committed_value_for_key_(self, *args, **kwargs):
        return self._ekevent.committedValueForKey_(*args, **kwargs)
    
    def compare_original_start_date_with_event_(self, *args, **kwargs):
        return self._ekevent.compareOriginalStartDateWithEvent_(*args, **kwargs)
    
    def compare_start_date_including_travel_with_event_(self, *args, **kwargs):
        return self._ekevent.compareStartDateIncludingTravelWithEvent_(*args, **kwargs)
    
    def compare_start_date_with_event_(self, *args, **kwargs):
        return self._ekevent.compareStartDateWithEvent_(*args, **kwargs)
    
    def completed(self, *args, **kwargs):
        return self._ekevent.completed(*args, **kwargs)
    
    def conference_u_r_l(self, *args, **kwargs):
        return self._ekevent.conferenceURL(*args, **kwargs)
    
    def conference_u_r_l_detected(self, *args, **kwargs):
        return self._ekevent.conferenceURLDetected(*args, **kwargs)
    
    def conference_u_r_l_detected_string(self, *args, **kwargs):
        return self._ekevent.conferenceURLDetectedString(*args, **kwargs)
    
    def conference_u_r_l_for_display(self, *args, **kwargs):
        return self._ekevent.conferenceURLForDisplay(*args, **kwargs)
    
    def conference_u_r_l_for_display_cached(self, *args, **kwargs):
        return self._ekevent.conferenceURLForDisplayCached(*args, **kwargs)
    
    def conference_u_r_l_string(self, *args, **kwargs):
        return self._ekevent.conferenceURLString(*args, **kwargs)
    
    def confirm_predicted_location_(self, *args, **kwargs):
        return self._ekevent.confirmPredictedLocation_(*args, **kwargs)
    
    def conforms_to_protocol_(self, *args, **kwargs):
        return self._ekevent.conformsToProtocol_(*args, **kwargs)
    
    def conforms_to_recurrence_rules_(self, *args, **kwargs):
        return self._ekevent.conformsToRecurrenceRules_(*args, **kwargs)
    
    def constraints(self, *args, **kwargs):
        return self._ekevent.constraints(*args, **kwargs)
    
    def constraints(self, *args, **kwargs):
        return self._ekevent.constraints(*args, **kwargs)
    
    def copy(self, *args, **kwargs):
        return self._ekevent.copy(*args, **kwargs)
    
    def copy_melted_object_cache(self, *args, **kwargs):
        return self._ekevent.copyMeltedObjectCache(*args, **kwargs)
    
    def copy_scripting_value_for_key_with_properties_(self, *args, **kwargs):
        return self._ekevent.copyScriptingValue_forKey_withProperties_(*args, **kwargs)
    
    def copy_to_calendar_with_options_(self, *args, **kwargs):
        return self._ekevent.copyToCalendar_withOptions_(*args, **kwargs)
    
    def copy_with_zone_(self, *args, **kwargs):
        return self._ekevent.copyWithZone_(*args, **kwargs)
    
    def could_be_junk(self, *args, **kwargs):
        return self._ekevent.couldBeJunk(*args, **kwargs)
    
    def count_of_attendee_proposed_times(self, *args, **kwargs):
        return self._ekevent.countOfAttendeeProposedTimes(*args, **kwargs)
    
    def create_key_value_binding_for_key_type_mask_(self, *args, **kwargs):
        return self._ekevent.createKeyValueBindingForKey_typeMask_(*args, **kwargs)
    
    def creation_date(self, *args, **kwargs):
        return self._ekevent.creationDate(*args, **kwargs)
    
    def current_user_generalized_participant_role(self, *args, **kwargs):
        return self._ekevent.currentUserGeneralizedParticipantRole(*args, **kwargs)
    
    def current_user_may_act_as_organizer(self, *args, **kwargs):
        return self._ekevent.currentUserMayActAsOrganizer(*args, **kwargs)
    
    def custom_object_for_key_(self, *args, **kwargs):
        return self._ekevent.customObjectForKey_(*args, **kwargs)
    
    def date_changed(self, *args, **kwargs):
        return self._ekevent.dateChanged(*args, **kwargs)
    
    def days_spanned_in_calendar_(self, *args, **kwargs):
        return self._ekevent.daysSpannedInCalendar_(*args, **kwargs)
    
    def dealloc(self, *args, **kwargs):
        return self._ekevent.dealloc(*args, **kwargs)
    
    def debug_description(self, *args, **kwargs):
        return self._ekevent.debugDescription(*args, **kwargs)
    
    def decline_proposed_time_notification_from_attendee_(self, *args, **kwargs):
        return self._ekevent.declineProposedTimeNotificationFromAttendee_(*args, **kwargs)
    
    def default_alarm(self, *args, **kwargs):
        return self._ekevent.defaultAlarm(*args, **kwargs)
    
    def default_alarm(self, *args, **kwargs):
        return self._ekevent.defaultAlarm(*args, **kwargs)
    
    def default_alarm_was_deleted(self, *args, **kwargs):
        return self._ekevent.defaultAlarmWasDeleted(*args, **kwargs)
    
    def default_alarms(self, *args, **kwargs):
        return self._ekevent.defaultAlarms(*args, **kwargs)
    
    def default_alarms(self, *args, **kwargs):
        return self._ekevent.defaultAlarms(*args, **kwargs)
    
    def delete_persistent_object(self, *args, **kwargs):
        return self._ekevent.deletePersistentObject(*args, **kwargs)
    
    def description(self, *args, **kwargs):
        return self._ekevent.description(*args, **kwargs)
    
    def description(self, *args, **kwargs):
        return self._ekevent.description(*args, **kwargs)
    
    def description(self, *args, **kwargs):
        return self._ekevent.description(*args, **kwargs)
    
    def description(self, *args, **kwargs):
        return self._ekevent.description(*args, **kwargs)
    
    def description_at_indent_(self, *args, **kwargs):
        return self._ekevent.descriptionAtIndent_(*args, **kwargs)
    
    def detached_items(self, *args, **kwargs):
        return self._ekevent.detachedItems(*args, **kwargs)
    
    def dictionary_with_values_for_keys_(self, *args, **kwargs):
        return self._ekevent.dictionaryWithValuesForKeys_(*args, **kwargs)
    
    def did_change_value_for_key_(self, *args, **kwargs):
        return self._ekevent.didChangeValueForKey_(*args, **kwargs)
    
    def did_change_value_for_key_with_set_mutation_using_objects_(self, *args, **kwargs):
        return self._ekevent.didChangeValueForKey_withSetMutation_usingObjects_(*args, **kwargs)
    
    def did_change_values_at_indexes_for_key_(self, *args, **kwargs):
        return self._ekevent.didChange_valuesAtIndexes_forKey_(*args, **kwargs)
    
    def diff_from_committed(self, *args, **kwargs):
        return self._ekevent.diffFromCommitted(*args, **kwargs)
    
    def diff_with_object_(self, *args, **kwargs):
        return self._ekevent.diffWithObject_(*args, **kwargs)
    
    def disallow_propose_new_time(self, *args, **kwargs):
        return self._ekevent.disallowProposeNewTime(*args, **kwargs)
    
    def dismiss_accepted_propose_new_time_notification(self, *args, **kwargs):
        return self._ekevent.dismissAcceptedProposeNewTimeNotification(*args, **kwargs)
    
    def dismiss_attendee_replied_notification(self, *args, **kwargs):
        return self._ekevent.dismissAttendeeRepliedNotification(*args, **kwargs)
    
    def display_notes(self, *args, **kwargs):
        return self._ekevent.displayNotes(*args, **kwargs)
    
    def display_notes(self, *args, **kwargs):
        return self._ekevent.displayNotes(*args, **kwargs)
    
    def does_contain_(self, *args, **kwargs):
        return self._ekevent.doesContain_(*args, **kwargs)
    
    def does_not_recognize_selector_(self, *args, **kwargs):
        return self._ekevent.doesNotRecognizeSelector_(*args, **kwargs)
    
    def does_not_recognize_selector_(self, *args, **kwargs):
        return self._ekevent.doesNotRecognizeSelector_(*args, **kwargs)
    
    def double_value_safe(self, *args, **kwargs):
        return self._ekevent.doubleValueSafe(*args, **kwargs)
    
    def double_value_safe_(self, *args, **kwargs):
        return self._ekevent.doubleValueSafe_(*args, **kwargs)
    
    def duplicate(self, *args, **kwargs):
        return self._ekevent.duplicate(*args, **kwargs)
    
    def duplicate_to_event_store_(self, *args, **kwargs):
        return self._ekevent.duplicateToEventStore_(*args, **kwargs)
    
    def duplicate_with_options_(self, *args, **kwargs):
        return self._ekevent.duplicateWithOptions_(*args, **kwargs)
    
    def duration(self, *args, **kwargs):
        return self._ekevent.duration(*args, **kwargs)
    
    def duration_including_travel(self, *args, **kwargs):
        return self._ekevent.durationIncludingTravel(*args, **kwargs)
    
    def duration_overlaps_recurrence_interval(self, *args, **kwargs):
        return self._ekevent.durationOverlapsRecurrenceInterval(*args, **kwargs)
    
    def earliest_occurrence_ending_after_(self, *args, **kwargs):
        return self._ekevent.earliestOccurrenceEndingAfter_(*args, **kwargs)
    
    def earliest_occurrence_ending_after_exclude_significant_detachments_exclude_canceled_detachments_exclude_declined_detachments_(self, *args, **kwargs):
        return self._ekevent.earliestOccurrenceEndingAfter_excludeSignificantDetachments_excludeCanceledDetachments_excludeDeclinedDetachments_(*args, **kwargs)
    
    def effective_time_zone(self, *args, **kwargs):
        return self._ekevent.effectiveTimeZone(*args, **kwargs)
    
    def ek_exception_dates(self, *args, **kwargs):
        return self._ekevent.ekExceptionDates(*args, **kwargs)
    
    def eligible_for_travel_advisories(self, *args, **kwargs):
        return self._ekevent.eligibleForTravelAdvisories(*args, **kwargs)
    
    def empty_melted_cache(self, *args, **kwargs):
        return self._ekevent.emptyMeltedCache(*args, **kwargs)
    
    def empty_melted_cache_for_key_(self, *args, **kwargs):
        return self._ekevent.emptyMeltedCacheForKey_(*args, **kwargs)
    
    def empty_melted_cache_for_keys_(self, *args, **kwargs):
        return self._ekevent.emptyMeltedCacheForKeys_(*args, **kwargs)
    
    def encode_with_c_a_m_l_writer_(self, *args, **kwargs):
        return self._ekevent.encodeWithCAMLWriter_(*args, **kwargs)
    
    def end_calendar_date(self, *args, **kwargs):
        return self._ekevent.endCalendarDate(*args, **kwargs)
    
    def end_date(self, *args, **kwargs):
        return self._ekevent.endDate(*args, **kwargs)
    
    def end_date_raw(self, *args, **kwargs):
        return self._ekevent.endDateRaw(*args, **kwargs)
    
    def end_date_unadjusted_for_legacy_clients(self, *args, **kwargs):
        return self._ekevent.endDateUnadjustedForLegacyClients(*args, **kwargs)
    
    def end_location(self, *args, **kwargs):
        return self._ekevent.endLocation(*args, **kwargs)
    
    def end_time_zone(self, *args, **kwargs):
        return self._ekevent.endTimeZone(*args, **kwargs)
    
    def end_time_zone_name(self, *args, **kwargs):
        return self._ekevent.endTimeZoneName(*args, **kwargs)
    
    def entity_name(self, *args, **kwargs):
        return self._ekevent.entityName(*args, **kwargs)
    
    def entity_type(self, *args, **kwargs):
        return self._ekevent.entityType(*args, **kwargs)
    
    def entity_type(self, *args, **kwargs):
        return self._ekevent.entityType(*args, **kwargs)
    
    def event_identifier(self, *args, **kwargs):
        return self._ekevent.eventIdentifier(*args, **kwargs)
    
    def event_occurrence_i_d(self, *args, **kwargs):
        return self._ekevent.eventOccurrenceID(*args, **kwargs)
    
    def event_store(self, *args, **kwargs):
        return self._ekevent.eventStore(*args, **kwargs)
    
    def exception_dates(self, *args, **kwargs):
        return self._ekevent.exceptionDates(*args, **kwargs)
    
    def exception_dates_adjusted_for_floating_events(self, *args, **kwargs):
        return self._ekevent.exceptionDatesAdjustedForFloatingEvents(*args, **kwargs)
    
    def existing_melted_object(self, *args, **kwargs):
        return self._ekevent.existingMeltedObject(*args, **kwargs)
    
    def exists_in_store(self, *args, **kwargs):
        return self._ekevent.existsInStore(*args, **kwargs)
    
    def export_to_i_c_s(self, *args, **kwargs):
        return self._ekevent.exportToICS(*args, **kwargs)
    
    def export_to_i_c_s_with_options_(self, *args, **kwargs):
        return self._ekevent.exportToICSWithOptions_(*args, **kwargs)
    
    def exposed_bindings(self, *args, **kwargs):
        return self._ekevent.exposedBindings(*args, **kwargs)
    
    def external_data(self, *args, **kwargs):
        return self._ekevent.externalData(*args, **kwargs)
    
    def external_i_d(self, *args, **kwargs):
        return self._ekevent.externalID(*args, **kwargs)
    
    def external_modification_tag(self, *args, **kwargs):
        return self._ekevent.externalModificationTag(*args, **kwargs)
    
    def external_schedule_i_d(self, *args, **kwargs):
        return self._ekevent.externalScheduleID(*args, **kwargs)
    
    def external_tracking_status(self, *args, **kwargs):
        return self._ekevent.externalTrackingStatus(*args, **kwargs)
    
    def external_u_r_i(self, *args, **kwargs):
        return self._ekevent.externalURI(*args, **kwargs)
    
    def external_u_r_i(self, *args, **kwargs):
        return self._ekevent.externalURI(*args, **kwargs)
    
    def external_u_r_l(self, *args, **kwargs):
        return self._ekevent.externalURL(*args, **kwargs)
    
    def filter_attendees_pending_deletion_(self, *args, **kwargs):
        return self._ekevent.filterAttendeesPendingDeletion_(*args, **kwargs)
    
    def finalize(self, *args, **kwargs):
        return self._ekevent.finalize(*args, **kwargs)
    
    def find_original_alarm_starting_with_(self, *args, **kwargs):
        return self._ekevent.findOriginalAlarmStartingWith_(*args, **kwargs)
    
    def finish_observing(self, *args, **kwargs):
        return self._ekevent.finishObserving(*args, **kwargs)
    
    def fired_t_t_l(self, *args, **kwargs):
        return self._ekevent.firedTTL(*args, **kwargs)
    
    def flag_(self, *args, **kwargs):
        return self._ekevent.flag_(*args, **kwargs)
    
    def flags(self, *args, **kwargs):
        return self._ekevent.flags(*args, **kwargs)
    
    def flush_key_bindings(self, *args, **kwargs):
        return self._ekevent.flushKeyBindings(*args, **kwargs)
    
    def force_location_prediction_update(self, *args, **kwargs):
        return self._ekevent.forceLocationPredictionUpdate(*args, **kwargs)
    
    def force_set_time_zone_(self, *args, **kwargs):
        return self._ekevent.forceSetTimeZone_(*args, **kwargs)
    
    def forward_invocation_(self, *args, **kwargs):
        return self._ekevent.forwardInvocation_(*args, **kwargs)
    
    def forwarding_target_for_selector_(self, *args, **kwargs):
        return self._ekevent.forwardingTargetForSelector_(*args, **kwargs)
    
    def fp__ivar_description_for_class_(self, *args, **kwargs):
        return self._ekevent.fp__ivarDescriptionForClass_(*args, **kwargs)
    
    def fp__method_description_for_class_(self, *args, **kwargs):
        return self._ekevent.fp__methodDescriptionForClass_(*args, **kwargs)
    
    def fp_ivar_description(self, *args, **kwargs):
        return self._ekevent.fp_ivarDescription(*args, **kwargs)
    
    def fp_method_description(self, *args, **kwargs):
        return self._ekevent.fp_methodDescription(*args, **kwargs)
    
    def fp_short_method_description(self, *args, **kwargs):
        return self._ekevent.fp_shortMethodDescription(*args, **kwargs)
    
    def frozen_class(self, *args, **kwargs):
        return self._ekevent.frozenClass(*args, **kwargs)
    
    def frozen_object(self, *args, **kwargs):
        return self._ekevent.frozenObject(*args, **kwargs)
    
    def frozen_object_in_store_(self, *args, **kwargs):
        return self._ekevent.frozenObjectInStore_(*args, **kwargs)
    
    def frozen_or_melted_cached_multi_relation_objects_for_key_(self, *args, **kwargs):
        return self._ekevent.frozenOrMeltedCachedMultiRelationObjectsForKey_(*args, **kwargs)
    
    def frozen_or_melted_cached_single_relation_object_for_key_(self, *args, **kwargs):
        return self._ekevent.frozenOrMeltedCachedSingleRelationObjectForKey_(*args, **kwargs)
    
    def future_occurrences_cannot_be_affected_by_changing_start_date_to_date_(self, *args, **kwargs):
        return self._ekevent.futureOccurrencesCannotBeAffectedByChangingStartDateToDate_(*args, **kwargs)
    
    def handle_query_with_unbound_key_(self, *args, **kwargs):
        return self._ekevent.handleQueryWithUnboundKey_(*args, **kwargs)
    
    def handle_take_value_for_unbound_key_(self, *args, **kwargs):
        return self._ekevent.handleTakeValue_forUnboundKey_(*args, **kwargs)
    
    def has_alarms(self, *args, **kwargs):
        return self._ekevent.hasAlarms(*args, **kwargs)
    
    def has_attachment(self, *args, **kwargs):
        return self._ekevent.hasAttachment(*args, **kwargs)
    
    def has_attachment_changes(self, *args, **kwargs):
        return self._ekevent.hasAttachmentChanges(*args, **kwargs)
    
    def has_attendee_proposed_times(self, *args, **kwargs):
        return self._ekevent.hasAttendeeProposedTimes(*args, **kwargs)
    
    def has_attendees(self, *args, **kwargs):
        return self._ekevent.hasAttendees(*args, **kwargs)
    
    def has_calendar_change_that_requires_delete_and_add(self, *args, **kwargs):
        return self._ekevent.hasCalendarChangeThatRequiresDeleteAndAdd(*args, **kwargs)
    
    def has_changes(self, *args, **kwargs):
        return self._ekevent.hasChanges(*args, **kwargs)
    
    def has_changes_requiring_span_all(self, *args, **kwargs):
        return self._ekevent.hasChangesRequiringSpanAll(*args, **kwargs)
    
    def has_complex_recurrence(self, *args, **kwargs):
        return self._ekevent.hasComplexRecurrence(*args, **kwargs)
    
    def has_ever_been_committed(self, *args, **kwargs):
        return self._ekevent.hasEverBeenCommitted(*args, **kwargs)
    
    def has_never_been_committed(self, *args, **kwargs):
        return self._ekevent.hasNeverBeenCommitted(*args, **kwargs)
    
    def has_notes(self, *args, **kwargs):
        return self._ekevent.hasNotes(*args, **kwargs)
    
    def has_predicted_location(self, *args, **kwargs):
        return self._ekevent.hasPredictedLocation(*args, **kwargs)
    
    def has_recurrence_rule_addition_or_removal(self, *args, **kwargs):
        return self._ekevent.hasRecurrenceRuleAdditionOrRemoval(*args, **kwargs)
    
    def has_recurrence_rules(self, *args, **kwargs):
        return self._ekevent.hasRecurrenceRules(*args, **kwargs)
    
    def has_unsaved_changes(self, *args, **kwargs):
        return self._ekevent.hasUnsavedChanges(*args, **kwargs)
    
    def has_unsaved_changes_ignore_keys_(self, *args, **kwargs):
        return self._ekevent.hasUnsavedChangesIgnoreKeys_(*args, **kwargs)
    
    def has_unsaved_changes_in_keys_(self, *args, **kwargs):
        return self._ekevent.hasUnsavedChangesInKeys_(*args, **kwargs)
    
    def has_valid_event_action(self, *args, **kwargs):
        return self._ekevent.hasValidEventAction(*args, **kwargs)
    
    def hash(self, *args, **kwargs):
        return self._ekevent.hash(*args, **kwargs)
    
    def hash(self, *args, **kwargs):
        return self._ekevent.hash(*args, **kwargs)
    
    def hash(self, *args, **kwargs):
        return self._ekevent.hash(*args, **kwargs)
    
    def if_set_value_if_non_nil_for_key_(self, *args, **kwargs):
        return self._ekevent.if_setValueIfNonNil_forKey_(*args, **kwargs)
    
    def if_set_value_if_y_e_s_for_key_(self, *args, **kwargs):
        return self._ekevent.if_setValueIfYES_forKey_(*args, **kwargs)
    
    def image(self, *args, **kwargs):
        return self._ekevent.image(*args, **kwargs)
    
    def implements_selector_(self, *args, **kwargs):
        return self._ekevent.implementsSelector_(*args, **kwargs)
    
    def index_for_alarm_(self, *args, **kwargs):
        return self._ekevent.indexForAlarm_(*args, **kwargs)
    
    def info_for_binding_(self, *args, **kwargs):
        return self._ekevent.infoForBinding_(*args, **kwargs)
    
    def init(self, *args, **kwargs):
        return self._ekevent.init(*args, **kwargs)
    
    def init(self, *args, **kwargs):
        return self._ekevent.init(*args, **kwargs)
    
    def init(self, *args, **kwargs):
        return self._ekevent.init(*args, **kwargs)
    
    def init_with_event_store_(self, *args, **kwargs):
        return self._ekevent.initWithEventStore_(*args, **kwargs)
    
    def init_with_persistent_object_(self, *args, **kwargs):
        return self._ekevent.initWithPersistentObject_(*args, **kwargs)
    
    def init_with_persistent_object_(self, *args, **kwargs):
        return self._ekevent.initWithPersistentObject_(*args, **kwargs)
    
    def init_with_persistent_object_object_for_copy_(self, *args, **kwargs):
        return self._ekevent.initWithPersistentObject_objectForCopy_(*args, **kwargs)
    
    def init_with_persistent_object_object_for_copy_(self, *args, **kwargs):
        return self._ekevent.initWithPersistentObject_objectForCopy_(*args, **kwargs)
    
    def init_with_persistent_object_occurrence_date_(self, *args, **kwargs):
        return self._ekevent.initWithPersistentObject_occurrenceDate_(*args, **kwargs)
    
    def initial_end_date(self, *args, **kwargs):
        return self._ekevent.initialEndDate(*args, **kwargs)
    
    def initial_start_date(self, *args, **kwargs):
        return self._ekevent.initialStartDate(*args, **kwargs)
    
    def insert_persistent_object_if_needed(self, *args, **kwargs):
        return self._ekevent.insertPersistentObjectIfNeeded(*args, **kwargs)
    
    def insert_value_at_index_in_property_with_key_(self, *args, **kwargs):
        return self._ekevent.insertValue_atIndex_inPropertyWithKey_(*args, **kwargs)
    
    def insert_value_in_property_with_key_(self, *args, **kwargs):
        return self._ekevent.insertValue_inPropertyWithKey_(*args, **kwargs)
    
    def int64_value_safe(self, *args, **kwargs):
        return self._ekevent.int64ValueSafe(*args, **kwargs)
    
    def int64_value_safe_(self, *args, **kwargs):
        return self._ekevent.int64ValueSafe_(*args, **kwargs)
    
    def invalidate_removed_virtual_conferences(self, *args, **kwargs):
        return self._ekevent.invalidateRemovedVirtualConferences(*args, **kwargs)
    
    def invalidate_virtual_conference_u_r_l_if_needed_on_commit_(self, *args, **kwargs):
        return self._ekevent.invalidateVirtualConferenceURLIfNeededOnCommit_(*args, **kwargs)
    
    def inverse_for_relationship_key_(self, *args, **kwargs):
        return self._ekevent.inverseForRelationshipKey_(*args, **kwargs)
    
    def inverse_object_with_object_diff_(self, *args, **kwargs):
        return self._ekevent.inverseObjectWithObject_diff_(*args, **kwargs)
    
    def invitation_changed_properties(self, *args, **kwargs):
        return self._ekevent.invitationChangedProperties(*args, **kwargs)
    
    def invitation_status(self, *args, **kwargs):
        return self._ekevent.invitationStatus(*args, **kwargs)
    
    def is_alarm_acknowledged_property_dirty(self, *args, **kwargs):
        return self._ekevent.isAlarmAcknowledgedPropertyDirty(*args, **kwargs)
    
    def is_alerted(self, *args, **kwargs):
        return self._ekevent.isAlerted(*args, **kwargs)
    
    def is_all_day(self, *args, **kwargs):
        return self._ekevent.isAllDay(*args, **kwargs)
    
    def is_all_day(self, *args, **kwargs):
        return self._ekevent.isAllDay(*args, **kwargs)
    
    def is_all_day_dirty(self, *args, **kwargs):
        return self._ekevent.isAllDayDirty(*args, **kwargs)
    
    def is_attendee_same_as_organizer_(self, *args, **kwargs):
        return self._ekevent.isAttendeeSameAsOrganizer_(*args, **kwargs)
    
    def is_birthday(self, *args, **kwargs):
        return self._ekevent.isBirthday(*args, **kwargs)
    
    def is_case_insensitive_like_(self, *args, **kwargs):
        return self._ekevent.isCaseInsensitiveLike_(*args, **kwargs)
    
    def is_completely_equal_(self, *args, **kwargs):
        return self._ekevent.isCompletelyEqual_(*args, **kwargs)
    
    def is_current_user_invited_attendee(self, *args, **kwargs):
        return self._ekevent.isCurrentUserInvitedAttendee(*args, **kwargs)
    
    def is_deletable(self, *args, **kwargs):
        return self._ekevent.isDeletable(*args, **kwargs)
    
    def is_deleted(self, *args, **kwargs):
        return self._ekevent.isDeleted(*args, **kwargs)
    
    def is_detached(self, *args, **kwargs):
        return self._ekevent.isDetached(*args, **kwargs)
    
    def is_different_and_has_forwarded_attendees_with_diff_(self, *args, **kwargs):
        return self._ekevent.isDifferentAndHasForwardedAttendeesWithDiff_(*args, **kwargs)
    
    def is_different_and_has_new_proposed_time_with_diff_(self, *args, **kwargs):
        return self._ekevent.isDifferentAndHasNewProposedTimeWithDiff_(*args, **kwargs)
    
    def is_different_and_has_unscheduled_attendees_with_diff_(self, *args, **kwargs):
        return self._ekevent.isDifferentAndHasUnscheduledAttendeesWithDiff_(*args, **kwargs)
    
    def is_different_and_modified_attendees_with_diff_(self, *args, **kwargs):
        return self._ekevent.isDifferentAndModifiedAttendeesWithDiff_(*args, **kwargs)
    
    def is_different_and_requires_r_s_v_p_with_diff_(self, *args, **kwargs):
        return self._ekevent.isDifferentAndRequiresRSVPWithDiff_(*args, **kwargs)
    
    def is_different_and_requires_reschedule_with_diff_(self, *args, **kwargs):
        return self._ekevent.isDifferentAndRequiresRescheduleWithDiff_(*args, **kwargs)
    
    def is_different_excepting_per_user_properties_with_diff_(self, *args, **kwargs):
        return self._ekevent.isDifferentExceptingPerUserPropertiesWithDiff_(*args, **kwargs)
    
    def is_different_from_committed(self, *args, **kwargs):
        return self._ekevent.isDifferentFromCommitted(*args, **kwargs)
    
    def is_different_from_committed_event_and_has_unscheduled_attendees(self, *args, **kwargs):
        return self._ekevent.isDifferentFromCommittedEventAndHasUnscheduledAttendees(*args, **kwargs)
    
    def is_different_from_committed_event_and_requires_r_s_v_p(self, *args, **kwargs):
        return self._ekevent.isDifferentFromCommittedEventAndRequiresRSVP(*args, **kwargs)
    
    def is_different_from_committed_event_and_requires_reschedule(self, *args, **kwargs):
        return self._ekevent.isDifferentFromCommittedEventAndRequiresReschedule(*args, **kwargs)
    
    def is_different_with_diff_(self, *args, **kwargs):
        return self._ekevent.isDifferentWithDiff_(*args, **kwargs)
    
    def is_editable(self, *args, **kwargs):
        return self._ekevent.isEditable(*args, **kwargs)
    
    def is_editable(self, *args, **kwargs):
        return self._ekevent.isEditable(*args, **kwargs)
    
    def is_end_date_dirty(self, *args, **kwargs):
        return self._ekevent.isEndDateDirty(*args, **kwargs)
    
    def is_equal_to_(self, *args, **kwargs):
        return self._ekevent.isEqualTo_(*args, **kwargs)
    
    def is_equal_(self, *args, **kwargs):
        return self._ekevent.isEqual_(*args, **kwargs)
    
    def is_equal_(self, *args, **kwargs):
        return self._ekevent.isEqual_(*args, **kwargs)
    
    def is_equal_(self, *args, **kwargs):
        return self._ekevent.isEqual_(*args, **kwargs)
    
    def is_equal_comparing_keys_(self, *args, **kwargs):
        return self._ekevent.isEqual_comparingKeys_(*args, **kwargs)
    
    def is_equal_comparing_keys_compare_immutable_keys_ignoring_properties_(self, *args, **kwargs):
        return self._ekevent.isEqual_comparingKeys_compareImmutableKeys_ignoringProperties_(*args, **kwargs)
    
    def is_equal_ignoring_properties_(self, *args, **kwargs):
        return self._ekevent.isEqual_ignoringProperties_(*args, **kwargs)
    
    def is_externally_organized_invitation(self, *args, **kwargs):
        return self._ekevent.isExternallyOrganizedInvitation(*args, **kwargs)
    
    def is_fault(self, *args, **kwargs):
        return self._ekevent.isFault(*args, **kwargs)
    
    def is_first_occurrence(self, *args, **kwargs):
        return self._ekevent.isFirstOccurrence(*args, **kwargs)
    
    def is_floating(self, *args, **kwargs):
        return self._ekevent.isFloating(*args, **kwargs)
    
    def is_floating(self, *args, **kwargs):
        return self._ekevent.isFloating(*args, **kwargs)
    
    def is_frozen(self, *args, **kwargs):
        return self._ekevent.isFrozen(*args, **kwargs)
    
    def is_greater_than_or_equal_to_(self, *args, **kwargs):
        return self._ekevent.isGreaterThanOrEqualTo_(*args, **kwargs)
    
    def is_greater_than_(self, *args, **kwargs):
        return self._ekevent.isGreaterThan_(*args, **kwargs)
    
    def is_kind_of_class_(self, *args, **kwargs):
        return self._ekevent.isKindOfClass_(*args, **kwargs)
    
    def is_less_than_or_equal_to_(self, *args, **kwargs):
        return self._ekevent.isLessThanOrEqualTo_(*args, **kwargs)
    
    def is_less_than_(self, *args, **kwargs):
        return self._ekevent.isLessThan_(*args, **kwargs)
    
    def is_like_(self, *args, **kwargs):
        return self._ekevent.isLike_(*args, **kwargs)
    
    def is_main_occurrence(self, *args, **kwargs):
        return self._ekevent.isMainOccurrence(*args, **kwargs)
    
    def is_master_or_detached_occurrence(self, *args, **kwargs):
        return self._ekevent.isMasterOrDetachedOccurrence(*args, **kwargs)
    
    def is_member_of_class_(self, *args, **kwargs):
        return self._ekevent.isMemberOfClass_(*args, **kwargs)
    
    def is_multi_day_timed_event_in_calendar_(self, *args, **kwargs):
        return self._ekevent.isMultiDayTimedEventInCalendar_(*args, **kwargs)
    
    def is_n_s_array__(self, *args, **kwargs):
        return self._ekevent.isNSArray__(*args, **kwargs)
    
    def is_n_s_c_f_constant_string__(self, *args, **kwargs):
        return self._ekevent.isNSCFConstantString__(*args, **kwargs)
    
    def is_n_s_data__(self, *args, **kwargs):
        return self._ekevent.isNSData__(*args, **kwargs)
    
    def is_n_s_date__(self, *args, **kwargs):
        return self._ekevent.isNSDate__(*args, **kwargs)
    
    def is_n_s_dictionary__(self, *args, **kwargs):
        return self._ekevent.isNSDictionary__(*args, **kwargs)
    
    def is_n_s_number__(self, *args, **kwargs):
        return self._ekevent.isNSNumber__(*args, **kwargs)
    
    def is_n_s_object__(self, *args, **kwargs):
        return self._ekevent.isNSObject__(*args, **kwargs)
    
    def is_n_s_ordered_set__(self, *args, **kwargs):
        return self._ekevent.isNSOrderedSet__(*args, **kwargs)
    
    def is_n_s_set__(self, *args, **kwargs):
        return self._ekevent.isNSSet__(*args, **kwargs)
    
    def is_n_s_string__(self, *args, **kwargs):
        return self._ekevent.isNSString__(*args, **kwargs)
    
    def is_n_s_time_zone__(self, *args, **kwargs):
        return self._ekevent.isNSTimeZone__(*args, **kwargs)
    
    def is_n_s_value__(self, *args, **kwargs):
        return self._ekevent.isNSValue__(*args, **kwargs)
    
    def is_new(self, *args, **kwargs):
        return self._ekevent.isNew(*args, **kwargs)
    
    def is_new_item_that_failed_to_put(self, *args, **kwargs):
        return self._ekevent.isNewItemThatFailedToPut(*args, **kwargs)
    
    def is_not_equal_to_(self, *args, **kwargs):
        return self._ekevent.isNotEqualTo_(*args, **kwargs)
    
    def is_null(self, *args, **kwargs):
        return self._ekevent.isNull(*args, **kwargs)
    
    def is_null(self, *args, **kwargs):
        return self._ekevent.isNull(*args, **kwargs)
    
    def is_null(self, *args, **kwargs):
        return self._ekevent.isNull(*args, **kwargs)
    
    def is_only_alarm_acknowledged_property_dirty(self, *args, **kwargs):
        return self._ekevent.isOnlyAlarmAcknowledgedPropertyDirty(*args, **kwargs)
    
    def is_only_occurrence(self, *args, **kwargs):
        return self._ekevent.isOnlyOccurrence(*args, **kwargs)
    
    def is_organized_by_shared_calendar_owner(self, *args, **kwargs):
        return self._ekevent.isOrganizedBySharedCalendarOwner(*args, **kwargs)
    
    def is_out_of_order_with_event_in_series(self, *args, **kwargs):
        return self._ekevent.isOutOfOrderWithEventInSeries(*args, **kwargs)
    
    def is_part_of_existing_recurring_series(self, *args, **kwargs):
        return self._ekevent.isPartOfExistingRecurringSeries(*args, **kwargs)
    
    def is_partial_object(self, *args, **kwargs):
        return self._ekevent.isPartialObject(*args, **kwargs)
    
    def is_phantom(self, *args, **kwargs):
        return self._ekevent.isPhantom(*args, **kwargs)
    
    def is_privacy_set(self, *args, **kwargs):
        return self._ekevent.isPrivacySet(*args, **kwargs)
    
    def is_private_event_shared_to_me(self, *args, **kwargs):
        return self._ekevent.isPrivateEventSharedToMe(*args, **kwargs)
    
    def is_property_unavailable_(self, *args, **kwargs):
        return self._ekevent.isPropertyUnavailable_(*args, **kwargs)
    
    def is_proposed_time_event(self, *args, **kwargs):
        return self._ekevent.isProposedTimeEvent(*args, **kwargs)
    
    def is_proxy(self, *args, **kwargs):
        return self._ekevent.isProxy(*args, **kwargs)
    
    def is_saved(self, *args, **kwargs):
        return self._ekevent.isSaved(*args, **kwargs)
    
    def is_self_organized(self, *args, **kwargs):
        return self._ekevent.isSelfOrganized(*args, **kwargs)
    
    def is_self_organized_invitation(self, *args, **kwargs):
        return self._ekevent.isSelfOrganizedInvitation(*args, **kwargs)
    
    def is_significantly_detached(self, *args, **kwargs):
        return self._ekevent.isSignificantlyDetached(*args, **kwargs)
    
    def is_significantly_detached_ignoring_participation(self, *args, **kwargs):
        return self._ekevent.isSignificantlyDetachedIgnoringParticipation(*args, **kwargs)
    
    def is_start_date_dirty(self, *args, **kwargs):
        return self._ekevent.isStartDateDirty(*args, **kwargs)
    
    def is_status_dirty(self, *args, **kwargs):
        return self._ekevent.isStatusDirty(*args, **kwargs)
    
    def is_tentative(self, *args, **kwargs):
        return self._ekevent.isTentative(*args, **kwargs)
    
    def is_to_many_key_(self, *args, **kwargs):
        return self._ekevent.isToManyKey_(*args, **kwargs)
    
    def is_undeleted(self, *args, **kwargs):
        return self._ekevent.isUndeleted(*args, **kwargs)
    
    def is_undetached(self, *args, **kwargs):
        return self._ekevent.isUndetached(*args, **kwargs)
    
    def is_valid_attendee_for_calendar_(self, *args, **kwargs):
        return self._ekevent.isValidAttendee_forCalendar_(*args, **kwargs)
    
    def junk_status(self, *args, **kwargs):
        return self._ekevent.junkStatus(*args, **kwargs)
    
    def key_value_binding_for_key_type_mask_(self, *args, **kwargs):
        return self._ekevent.keyValueBindingForKey_typeMask_(*args, **kwargs)
    
    def last_modified_date(self, *args, **kwargs):
        return self._ekevent.lastModifiedDate(*args, **kwargs)
    
    def launch_u_r_l(self, *args, **kwargs):
        return self._ekevent.launchURL(*args, **kwargs)
    
    def local_custom_object_for_key_(self, *args, **kwargs):
        return self._ekevent.localCustomObjectForKey_(*args, **kwargs)
    
    def local_structured_data(self, *args, **kwargs):
        return self._ekevent.localStructuredData(*args, **kwargs)
    
    def local_u_i_d(self, *args, **kwargs):
        return self._ekevent.localUID(*args, **kwargs)
    
    def location(self, *args, **kwargs):
        return self._ekevent.location(*args, **kwargs)
    
    def location_changed(self, *args, **kwargs):
        return self._ekevent.locationChanged(*args, **kwargs)
    
    def location_is_a_conference_room(self, *args, **kwargs):
        return self._ekevent.locationIsAConferenceRoom(*args, **kwargs)
    
    def location_prediction_state(self, *args, **kwargs):
        return self._ekevent.locationPredictionState(*args, **kwargs)
    
    def location_without_prediction(self, *args, **kwargs):
        return self._ekevent.locationWithoutPrediction(*args, **kwargs)
    
    def locations(self, *args, **kwargs):
        return self._ekevent.locations(*args, **kwargs)
    
    def locations_without_prediction(self, *args, **kwargs):
        return self._ekevent.locationsWithoutPrediction(*args, **kwargs)
    
    def lunar_calendar_string(self, *args, **kwargs):
        return self._ekevent.lunarCalendarString(*args, **kwargs)
    
    def make_recurrence_end_count_based(self, *args, **kwargs):
        return self._ekevent.makeRecurrenceEndCountBased(*args, **kwargs)
    
    def make_recurrence_end_date_based(self, *args, **kwargs):
        return self._ekevent.makeRecurrenceEndDateBased(*args, **kwargs)
    
    def mark_as_committed(self, *args, **kwargs):
        return self._ekevent.markAsCommitted(*args, **kwargs)
    
    def mark_as_committed(self, *args, **kwargs):
        return self._ekevent.markAsCommitted(*args, **kwargs)
    
    def mark_as_deleted(self, *args, **kwargs):
        return self._ekevent.markAsDeleted(*args, **kwargs)
    
    def mark_as_new(self, *args, **kwargs):
        return self._ekevent.markAsNew(*args, **kwargs)
    
    def mark_as_not_new(self, *args, **kwargs):
        return self._ekevent.markAsNotNew(*args, **kwargs)
    
    def mark_as_saved(self, *args, **kwargs):
        return self._ekevent.markAsSaved(*args, **kwargs)
    
    def mark_as_saved(self, *args, **kwargs):
        return self._ekevent.markAsSaved(*args, **kwargs)
    
    def mark_as_undeleted(self, *args, **kwargs):
        return self._ekevent.markAsUndeleted(*args, **kwargs)
    
    def mark_as_undeleted(self, *args, **kwargs):
        return self._ekevent.markAsUndeleted(*args, **kwargs)
    
    def mark_as_undetached_with_start_date_end_date_(self, *args, **kwargs):
        return self._ekevent.markAsUndetachedWithStartDate_endDate_(*args, **kwargs)
    
    def mark_event_as_attendee_forward(self, *args, **kwargs):
        return self._ekevent.markEventAsAttendeeForward(*args, **kwargs)
    
    def master_event(self, *args, **kwargs):
        return self._ekevent.masterEvent(*args, **kwargs)
    
    def melted_and_cached_multi_relation_count_for_key_(self, *args, **kwargs):
        return self._ekevent.meltedAndCachedMultiRelationCountForKey_(*args, **kwargs)
    
    def melted_and_cached_multi_relation_objects_for_key_(self, *args, **kwargs):
        return self._ekevent.meltedAndCachedMultiRelationObjectsForKey_(*args, **kwargs)
    
    def melted_and_cached_single_relation_object_for_key_(self, *args, **kwargs):
        return self._ekevent.meltedAndCachedSingleRelationObjectForKey_(*args, **kwargs)
    
    def melted_object_in_store_(self, *args, **kwargs):
        return self._ekevent.meltedObjectInStore_(*args, **kwargs)
    
    def method_description_for_selector_(self, *args, **kwargs):
        return self._ekevent.methodDescriptionForSelector_(*args, **kwargs)
    
    def method_for_selector_(self, *args, **kwargs):
        return self._ekevent.methodForSelector_(*args, **kwargs)
    
    def method_signature_for_selector_(self, *args, **kwargs):
        return self._ekevent.methodSignatureForSelector_(*args, **kwargs)
    
    def method_signature_for_selector_(self, *args, **kwargs):
        return self._ekevent.methodSignatureForSelector_(*args, **kwargs)
    
    def modified_properties(self, *args, **kwargs):
        return self._ekevent.modifiedProperties(*args, **kwargs)
    
    def move_to_calendar_(self, *args, **kwargs):
        return self._ekevent.moveToCalendar_(*args, **kwargs)
    
    def mr_formatted_debug_description(self, *args, **kwargs):
        return self._ekevent.mr_formattedDebugDescription(*args, **kwargs)
    
    def multi_changed_object_values_for_key_(self, *args, **kwargs):
        return self._ekevent.multiChangedObjectValuesForKey_(*args, **kwargs)
    
    def mutable_array_value_for_key_path_(self, *args, **kwargs):
        return self._ekevent.mutableArrayValueForKeyPath_(*args, **kwargs)
    
    def mutable_array_value_for_key_(self, *args, **kwargs):
        return self._ekevent.mutableArrayValueForKey_(*args, **kwargs)
    
    def mutable_copy(self, *args, **kwargs):
        return self._ekevent.mutableCopy(*args, **kwargs)
    
    def mutable_copy_with_zone_(self, *args, **kwargs):
        return self._ekevent.mutableCopyWithZone_(*args, **kwargs)
    
    def mutable_ordered_set_value_for_key_path_(self, *args, **kwargs):
        return self._ekevent.mutableOrderedSetValueForKeyPath_(*args, **kwargs)
    
    def mutable_ordered_set_value_for_key_(self, *args, **kwargs):
        return self._ekevent.mutableOrderedSetValueForKey_(*args, **kwargs)
    
    def mutable_set_value_for_key_path_(self, *args, **kwargs):
        return self._ekevent.mutableSetValueForKeyPath_(*args, **kwargs)
    
    def mutable_set_value_for_key_(self, *args, **kwargs):
        return self._ekevent.mutableSetValueForKey_(*args, **kwargs)
    
    def needs_geocoding(self, *args, **kwargs):
        return self._ekevent.needsGeocoding(*args, **kwargs)
    
    def needs_response(self, *args, **kwargs):
        return self._ekevent.needsResponse(*args, **kwargs)
    
    def new_scripting_object_of_class_for_value_for_key_with_contents_value_properties_(self, *args, **kwargs):
        return self._ekevent.newScriptingObjectOfClass_forValueForKey_withContentsValue_properties_(*args, **kwargs)
    
    def new_tagged_n_s_string_with_a_s_c_i_i_bytes__length__(self, *args, **kwargs):
        return self._ekevent.newTaggedNSStringWithASCIIBytes__length__(*args, **kwargs)
    
    def next_occurrence_or_detachment_after_(self, *args, **kwargs):
        return self._ekevent.nextOccurrenceOrDetachmentAfter_(*args, **kwargs)
    
    def notes(self, *args, **kwargs):
        return self._ekevent.notes(*args, **kwargs)
    
    def object_i_d(self, *args, **kwargs):
        return self._ekevent.objectID(*args, **kwargs)
    
    def object_specifier(self, *args, **kwargs):
        return self._ekevent.objectSpecifier(*args, **kwargs)
    
    def observation_info(self, *args, **kwargs):
        return self._ekevent.observationInfo(*args, **kwargs)
    
    def observe_value_for_key_path_of_object_change_context_(self, *args, **kwargs):
        return self._ekevent.observeValueForKeyPath_ofObject_change_context_(*args, **kwargs)
    
    def occurrence_date(self, *args, **kwargs):
        return self._ekevent.occurrenceDate(*args, **kwargs)
    
    def occurrence_end_date(self, *args, **kwargs):
        return self._ekevent.occurrenceEndDate(*args, **kwargs)
    
    def occurrence_is_all_day(self, *args, **kwargs):
        return self._ekevent.occurrenceIsAllDay(*args, **kwargs)
    
    def occurrence_start_date(self, *args, **kwargs):
        return self._ekevent.occurrenceStartDate(*args, **kwargs)
    
    def option_descriptions_for_binding_(self, *args, **kwargs):
        return self._ekevent.optionDescriptionsForBinding_(*args, **kwargs)
    
    def organized_by_me(self, *args, **kwargs):
        return self._ekevent.organizedByMe(*args, **kwargs)
    
    def organizer(self, *args, **kwargs):
        return self._ekevent.organizer(*args, **kwargs)
    
    def original_item(self, *args, **kwargs):
        return self._ekevent.originalItem(*args, **kwargs)
    
    def original_occurrence_end_date(self, *args, **kwargs):
        return self._ekevent.originalOccurrenceEndDate(*args, **kwargs)
    
    def original_occurrence_is_all_day(self, *args, **kwargs):
        return self._ekevent.originalOccurrenceIsAllDay(*args, **kwargs)
    
    def original_occurrence_start_date(self, *args, **kwargs):
        return self._ekevent.originalOccurrenceStartDate(*args, **kwargs)
    
    def original_start_date(self, *args, **kwargs):
        return self._ekevent.originalStartDate(*args, **kwargs)
    
    def overlaps_with_or_is_same_day_as_event_in_series(self, *args, **kwargs):
        return self._ekevent.overlapsWithOrIsSameDayAsEventInSeries(*args, **kwargs)
    
    def override_end_date_(self, *args, **kwargs):
        return self._ekevent.overrideEndDate_(*args, **kwargs)
    
    def override_start_date_(self, *args, **kwargs):
        return self._ekevent.overrideStartDate_(*args, **kwargs)
    
    def owns_destination_objects_for_relationship_key_(self, *args, **kwargs):
        return self._ekevent.ownsDestinationObjectsForRelationshipKey_(*args, **kwargs)
    
    def parsed_conference_and_notes_(self, *args, **kwargs):
        return self._ekevent.parsedConference_andNotes_(*args, **kwargs)
    
    def participant_matching_contact_(self, *args, **kwargs):
        return self._ekevent.participantMatchingContact_(*args, **kwargs)
    
    def participation_status(self, *args, **kwargs):
        return self._ekevent.participationStatus(*args, **kwargs)
    
    def participation_status_modified_date(self, *args, **kwargs):
        return self._ekevent.participationStatusModifiedDate(*args, **kwargs)
    
    def pending_participation_status(self, *args, **kwargs):
        return self._ekevent.pendingParticipationStatus(*args, **kwargs)
    
    def pep_after_delay_(self, *args, **kwargs):
        return self._ekevent.pep_afterDelay_(*args, **kwargs)
    
    def pep_get_invocation_(self, *args, **kwargs):
        return self._ekevent.pep_getInvocation_(*args, **kwargs)
    
    def pep_on_main_thread(self, *args, **kwargs):
        return self._ekevent.pep_onMainThread(*args, **kwargs)
    
    def pep_on_main_thread_if_necessary(self, *args, **kwargs):
        return self._ekevent.pep_onMainThreadIfNecessary(*args, **kwargs)
    
    def pep_on_operation_queue_(self, *args, **kwargs):
        return self._ekevent.pep_onOperationQueue_(*args, **kwargs)
    
    def pep_on_operation_queue_priority_(self, *args, **kwargs):
        return self._ekevent.pep_onOperationQueue_priority_(*args, **kwargs)
    
    def pep_on_thread_(self, *args, **kwargs):
        return self._ekevent.pep_onThread_(*args, **kwargs)
    
    def pep_on_thread_immediate_for_matching_thread_(self, *args, **kwargs):
        return self._ekevent.pep_onThread_immediateForMatchingThread_(*args, **kwargs)
    
    def perform_block_on_main_thread_synchronously_(self, *args, **kwargs):
        return self._ekevent.performBlockOnMainThreadSynchronously_(*args, **kwargs)
    
    def perform_selector_in_background_with_object_(self, *args, **kwargs):
        return self._ekevent.performSelectorInBackground_withObject_(*args, **kwargs)
    
    def perform_selector_on_main_thread_with_object_wait_until_done_(self, *args, **kwargs):
        return self._ekevent.performSelectorOnMainThread_withObject_waitUntilDone_(*args, **kwargs)
    
    def perform_selector_on_main_thread_with_object_wait_until_done_modes_(self, *args, **kwargs):
        return self._ekevent.performSelectorOnMainThread_withObject_waitUntilDone_modes_(*args, **kwargs)
    
    def perform_selector_(self, *args, **kwargs):
        return self._ekevent.performSelector_(*args, **kwargs)
    
    def perform_selector_object_after_delay_(self, *args, **kwargs):
        return self._ekevent.performSelector_object_afterDelay_(*args, **kwargs)
    
    def perform_selector_on_thread_with_object_wait_until_done_(self, *args, **kwargs):
        return self._ekevent.performSelector_onThread_withObject_waitUntilDone_(*args, **kwargs)
    
    def perform_selector_on_thread_with_object_wait_until_done_modes_(self, *args, **kwargs):
        return self._ekevent.performSelector_onThread_withObject_waitUntilDone_modes_(*args, **kwargs)
    
    def perform_selector_with_object_(self, *args, **kwargs):
        return self._ekevent.performSelector_withObject_(*args, **kwargs)
    
    def perform_selector_with_object_after_delay_(self, *args, **kwargs):
        return self._ekevent.performSelector_withObject_afterDelay_(*args, **kwargs)
    
    def perform_selector_with_object_after_delay_ignore_menu_tracking_(self, *args, **kwargs):
        return self._ekevent.performSelector_withObject_afterDelay_ignoreMenuTracking_(*args, **kwargs)
    
    def perform_selector_with_object_after_delay_in_modes_(self, *args, **kwargs):
        return self._ekevent.performSelector_withObject_afterDelay_inModes_(*args, **kwargs)
    
    def perform_selector_with_object_with_object_(self, *args, **kwargs):
        return self._ekevent.performSelector_withObject_withObject_(*args, **kwargs)
    
    def persistent_object(self, *args, **kwargs):
        return self._ekevent.persistentObject(*args, **kwargs)
    
    def phantom_master(self, *args, **kwargs):
        return self._ekevent.phantomMaster(*args, **kwargs)
    
    def post_modified_notification(self, *args, **kwargs):
        return self._ekevent.postModifiedNotification(*args, **kwargs)
    
    def post_modified_notification_with_user_info_(self, *args, **kwargs):
        return self._ekevent.postModifiedNotificationWithUserInfo_(*args, **kwargs)
    
    def potential_conflict_occurrence_dates_in_time_period_(self, *args, **kwargs):
        return self._ekevent.potentialConflictOccurrenceDatesInTimePeriod_(*args, **kwargs)
    
    def potentially_eligible_for_travel_advisories(self, *args, **kwargs):
        return self._ekevent.potentiallyEligibleForTravelAdvisories(*args, **kwargs)
    
    def pre_frozen_relationship_objects(self, *args, **kwargs):
        return self._ekevent.preFrozenRelationshipObjects(*args, **kwargs)
    
    def preferred_location(self, *args, **kwargs):
        return self._ekevent.preferredLocation(*args, **kwargs)
    
    def preferred_location_without_prediction(self, *args, **kwargs):
        return self._ekevent.preferredLocationWithoutPrediction(*args, **kwargs)
    
    def prepare_for_interface_builder(self, *args, **kwargs):
        return self._ekevent.prepareForInterfaceBuilder(*args, **kwargs)
    
    def prepare_reminder_kit_object_for_save_with_updated_backing_object_provider_(self, *args, **kwargs):
        return self._ekevent.prepareReminderKitObjectForSaveWithUpdatedBackingObjectProvider_(*args, **kwargs)
    
    def prevent_conference_u_r_l_detection(self, *args, **kwargs):
        return self._ekevent.preventConferenceURLDetection(*args, **kwargs)
    
    def previously_saved_copy(self, *args, **kwargs):
        return self._ekevent.previouslySavedCopy(*args, **kwargs)
    
    def previously_saved_copy(self, *args, **kwargs):
        return self._ekevent.previouslySavedCopy(*args, **kwargs)
    
    def priority(self, *args, **kwargs):
        return self._ekevent.priority(*args, **kwargs)
    
    def privacy_description(self, *args, **kwargs):
        return self._ekevent.privacyDescription(*args, **kwargs)
    
    def privacy_description(self, *args, **kwargs):
        return self._ekevent.privacyDescription(*args, **kwargs)
    
    def privacy_level(self, *args, **kwargs):
        return self._ekevent.privacyLevel(*args, **kwargs)
    
    def privacy_level_string(self, *args, **kwargs):
        return self._ekevent.privacyLevelString(*args, **kwargs)
    
    def proposed_end_date(self, *args, **kwargs):
        return self._ekevent.proposedEndDate(*args, **kwargs)
    
    def proposed_start_date(self, *args, **kwargs):
        return self._ekevent.proposedStartDate(*args, **kwargs)
    
    def rebase(self, *args, **kwargs):
        return self._ekevent.rebase(*args, **kwargs)
    
    def rebase_skipping_relation_properties_(self, *args, **kwargs):
        return self._ekevent.rebaseSkippingRelationProperties_(*args, **kwargs)
    
    def rebase_skipping_relation_properties_(self, *args, **kwargs):
        return self._ekevent.rebaseSkippingRelationProperties_(*args, **kwargs)
    
    def rebase_skipping_relation_properties_to_event_store_(self, *args, **kwargs):
        return self._ekevent.rebaseSkippingRelationProperties_toEventStore_(*args, **kwargs)
    
    def rebase_to_event_store_(self, *args, **kwargs):
        return self._ekevent.rebaseToEventStore_(*args, **kwargs)
    
    def rebase_to_event_store_(self, *args, **kwargs):
        return self._ekevent.rebaseToEventStore_(*args, **kwargs)
    
    def rebased_from(self, *args, **kwargs):
        return self._ekevent.rebasedFrom(*args, **kwargs)
    
    def receive_observed_error_(self, *args, **kwargs):
        return self._ekevent.receiveObservedError_(*args, **kwargs)
    
    def receive_observed_value_(self, *args, **kwargs):
        return self._ekevent.receiveObservedValue_(*args, **kwargs)
    
    def recurrence_changed(self, *args, **kwargs):
        return self._ekevent.recurrenceChanged(*args, **kwargs)
    
    def recurrence_date(self, *args, **kwargs):
        return self._ekevent.recurrenceDate(*args, **kwargs)
    
    def recurrence_identifier(self, *args, **kwargs):
        return self._ekevent.recurrenceIdentifier(*args, **kwargs)
    
    def recurrence_rule(self, *args, **kwargs):
        return self._ekevent.recurrenceRule(*args, **kwargs)
    
    def recurrence_rule_string(self, *args, **kwargs):
        return self._ekevent.recurrenceRuleString(*args, **kwargs)
    
    def recurrence_rules(self, *args, **kwargs):
        return self._ekevent.recurrenceRules(*args, **kwargs)
    
    def recurrence_rules_set(self, *args, **kwargs):
        return self._ekevent.recurrenceRulesSet(*args, **kwargs)
    
    def recurrence_set(self, *args, **kwargs):
        return self._ekevent.recurrenceSet(*args, **kwargs)
    
    def refetch(self, *args, **kwargs):
        return self._ekevent.refetch(*args, **kwargs)
    
    def refresh(self, *args, **kwargs):
        return self._ekevent.refresh(*args, **kwargs)
    
    def refresh(self, *args, **kwargs):
        return self._ekevent.refresh(*args, **kwargs)
    
    def refresh_and_notify_(self, *args, **kwargs):
        return self._ekevent.refreshAndNotify_(*args, **kwargs)
    
    def refresh_and_notify_(self, *args, **kwargs):
        return self._ekevent.refreshAndNotify_(*args, **kwargs)
    
    def reject_predicted_location(self, *args, **kwargs):
        return self._ekevent.rejectPredictedLocation(*args, **kwargs)
    
    def release(self, *args, **kwargs):
        return self._ekevent.release(*args, **kwargs)
    
    def remove_acknowledged_snoozed_alarms(self, *args, **kwargs):
        return self._ekevent.removeAcknowledgedSnoozedAlarms(*args, **kwargs)
    
    def remove_alarm_(self, *args, **kwargs):
        return self._ekevent.removeAlarm_(*args, **kwargs)
    
    def remove_all_snoozed_alarms(self, *args, **kwargs):
        return self._ekevent.removeAllSnoozedAlarms(*args, **kwargs)
    
    def remove_attachment_(self, *args, **kwargs):
        return self._ekevent.removeAttachment_(*args, **kwargs)
    
    def remove_attendee_(self, *args, **kwargs):
        return self._ekevent.removeAttendee_(*args, **kwargs)
    
    def remove_cached_melted_object_for_multi_value_key_(self, *args, **kwargs):
        return self._ekevent.removeCachedMeltedObject_forMultiValueKey_(*args, **kwargs)
    
    def remove_conference_rooms_(self, *args, **kwargs):
        return self._ekevent.removeConferenceRooms_(*args, **kwargs)
    
    def remove_event_action_(self, *args, **kwargs):
        return self._ekevent.removeEventAction_(*args, **kwargs)
    
    def remove_last_extraneous_organizer_and_self_attendee(self, *args, **kwargs):
        return self._ekevent.removeLastExtraneousOrganizerAndSelfAttendee(*args, **kwargs)
    
    def remove_multi_changed_object_value_for_key_(self, *args, **kwargs):
        return self._ekevent.removeMultiChangedObjectValue_forKey_(*args, **kwargs)
    
    def remove_multi_changed_object_values_for_key_(self, *args, **kwargs):
        return self._ekevent.removeMultiChangedObjectValues_forKey_(*args, **kwargs)
    
    def remove_object_from_both_sides_of_relationship_with_key_(self, *args, **kwargs):
        return self._ekevent.removeObject_fromBothSidesOfRelationshipWithKey_(*args, **kwargs)
    
    def remove_object_from_property_with_key_(self, *args, **kwargs):
        return self._ekevent.removeObject_fromPropertyWithKey_(*args, **kwargs)
    
    def remove_observation_(self, *args, **kwargs):
        return self._ekevent.removeObservation_(*args, **kwargs)
    
    def remove_observation_for_observable_key_path_(self, *args, **kwargs):
        return self._ekevent.removeObservation_forObservableKeyPath_(*args, **kwargs)
    
    def remove_observer_for_key_path_(self, *args, **kwargs):
        return self._ekevent.removeObserver_forKeyPath_(*args, **kwargs)
    
    def remove_observer_for_key_path_context_(self, *args, **kwargs):
        return self._ekevent.removeObserver_forKeyPath_context_(*args, **kwargs)
    
    def remove_recurrence_rule_(self, *args, **kwargs):
        return self._ekevent.removeRecurrenceRule_(*args, **kwargs)
    
    def remove_server_refresh_related_properties(self, *args, **kwargs):
        return self._ekevent.removeServerRefreshRelatedProperties(*args, **kwargs)
    
    def remove_value_at_index_from_property_with_key_(self, *args, **kwargs):
        return self._ekevent.removeValueAtIndex_fromPropertyWithKey_(*args, **kwargs)
    
    def remove_with_span_error_(self, *args, **kwargs):
        return self._ekevent.removeWithSpan_error_(*args, **kwargs)
    
    def replace_multi_changed_object_values_with_object_values_for_key_(self, *args, **kwargs):
        return self._ekevent.replaceMultiChangedObjectValuesWithObjectValues_forKey_(*args, **kwargs)
    
    def replace_value_at_index_in_property_with_key_with_value_(self, *args, **kwargs):
        return self._ekevent.replaceValueAtIndex_inPropertyWithKey_withValue_(*args, **kwargs)
    
    def replacement_object_for_archiver_(self, *args, **kwargs):
        return self._ekevent.replacementObjectForArchiver_(*args, **kwargs)
    
    def replacement_object_for_coder_(self, *args, **kwargs):
        return self._ekevent.replacementObjectForCoder_(*args, **kwargs)
    
    def replacement_object_for_keyed_archiver_(self, *args, **kwargs):
        return self._ekevent.replacementObjectForKeyedArchiver_(*args, **kwargs)
    
    def replacement_object_for_port_coder_(self, *args, **kwargs):
        return self._ekevent.replacementObjectForPortCoder_(*args, **kwargs)
    
    def requirements_to_move_from_calendar_to_calendar_(self, *args, **kwargs):
        return self._ekevent.requirementsToMoveFromCalendar_toCalendar_(*args, **kwargs)
    
    def requirements_to_move_to_calendar_(self, *args, **kwargs):
        return self._ekevent.requirementsToMoveToCalendar_(*args, **kwargs)
    
    def requires_copy_to_move_from_calendar_to_calendar_(self, *args, **kwargs):
        return self._ekevent.requiresCopyToMoveFromCalendar_toCalendar_(*args, **kwargs)
    
    def requires_detach(self, *args, **kwargs):
        return self._ekevent.requiresDetach(*args, **kwargs)
    
    def requires_detach(self, *args, **kwargs):
        return self._ekevent.requiresDetach(*args, **kwargs)
    
    def requires_detach_due_to_snoozed_alarm(self, *args, **kwargs):
        return self._ekevent.requiresDetachDueToSnoozedAlarm(*args, **kwargs)
    
    def reset(self, *args, **kwargs):
        return self._ekevent.reset(*args, **kwargs)
    
    def reset(self, *args, **kwargs):
        return self._ekevent.reset(*args, **kwargs)
    
    def responds_to_selector_(self, *args, **kwargs):
        return self._ekevent.respondsToSelector_(*args, **kwargs)
    
    def response_comment(self, *args, **kwargs):
        return self._ekevent.responseComment(*args, **kwargs)
    
    def response_must_apply_to_all(self, *args, **kwargs):
        return self._ekevent.responseMustApplyToAll(*args, **kwargs)
    
    def retain(self, *args, **kwargs):
        return self._ekevent.retain(*args, **kwargs)
    
    def retain_count(self, *args, **kwargs):
        return self._ekevent.retainCount(*args, **kwargs)
    
    def retain_weak_reference(self, *args, **kwargs):
        return self._ekevent.retainWeakReference(*args, **kwargs)
    
    def revert(self, *args, **kwargs):
        return self._ekevent.revert(*args, **kwargs)
    
    def revert(self, *args, **kwargs):
        return self._ekevent.revert(*args, **kwargs)
    
    def rollback(self, *args, **kwargs):
        return self._ekevent.rollback(*args, **kwargs)
    
    def rollback(self, *args, **kwargs):
        return self._ekevent.rollback(*args, **kwargs)
    
    def room_attendees(self, *args, **kwargs):
        return self._ekevent.roomAttendees(*args, **kwargs)
    
    def row_i_d(self, *args, **kwargs):
        return self._ekevent.rowID(*args, **kwargs)
    
    def save_with_span_error_(self, *args, **kwargs):
        return self._ekevent.saveWithSpan_error_(*args, **kwargs)
    
    def scan_for_conflicts(self, *args, **kwargs):
        return self._ekevent.scanForConflicts(*args, **kwargs)
    
    def scripting_properties(self, *args, **kwargs):
        return self._ekevent.scriptingProperties(*args, **kwargs)
    
    def scripting_value_for_specifier_(self, *args, **kwargs):
        return self._ekevent.scriptingValueForSpecifier_(*args, **kwargs)
    
    def self(self, *args, **kwargs):
        return self._ekevent.self(*args, **kwargs)
    
    def self_attendee(self, *args, **kwargs):
        return self._ekevent.selfAttendee(*args, **kwargs)
    
    def self_participant_status(self, *args, **kwargs):
        return self._ekevent.selfParticipantStatus(*args, **kwargs)
    
    def self_participant_status(self, *args, **kwargs):
        return self._ekevent.selfParticipantStatus(*args, **kwargs)
    
    def self_participant_status_raw(self, *args, **kwargs):
        return self._ekevent.selfParticipantStatusRaw(*args, **kwargs)
    
    def semantic_identifier(self, *args, **kwargs):
        return self._ekevent.semanticIdentifier(*args, **kwargs)
    
    def senders_email(self, *args, **kwargs):
        return self._ekevent.sendersEmail(*args, **kwargs)
    
    def senders_phone_number(self, *args, **kwargs):
        return self._ekevent.sendersPhoneNumber(*args, **kwargs)
    
    def sequence_number(self, *args, **kwargs):
        return self._ekevent.sequenceNumber(*args, **kwargs)
    
    def series_has_out_of_order_events(self, *args, **kwargs):
        return self._ekevent.seriesHasOutOfOrderEvents(*args, **kwargs)
    
    def series_has_overlapping_or_on_same_day_or_out_of_order_events(self, *args, **kwargs):
        return self._ekevent.seriesHasOverlappingOrOnSameDayOrOutOfOrderEvents(*args, **kwargs)
    
    def server_supported_propose_new_time(self, *args, **kwargs):
        return self._ekevent.serverSupportedProposeNewTime(*args, **kwargs)
    
    def set_accessibility_braille_map_render_region_(self, *args, **kwargs):
        return self._ekevent.setAccessibilityBrailleMapRenderRegion_(*args, **kwargs)
    
    def set_accessibility_braille_map_renderer_(self, *args, **kwargs):
        return self._ekevent.setAccessibilityBrailleMapRenderer_(*args, **kwargs)
    
    def set_action_string_(self, *args, **kwargs):
        return self._ekevent.setActionString_(*args, **kwargs)
    
    def set_action_(self, *args, **kwargs):
        return self._ekevent.setAction_(*args, **kwargs)
    
    def set_actions_(self, *args, **kwargs):
        return self._ekevent.setActions_(*args, **kwargs)
    
    def set_additional_frozen_properties_(self, *args, **kwargs):
        return self._ekevent.setAdditionalFrozenProperties_(*args, **kwargs)
    
    def set_additional_melted_objects_(self, *args, **kwargs):
        return self._ekevent.setAdditionalMeltedObjects_(*args, **kwargs)
    
    def set_alarms_(self, *args, **kwargs):
        return self._ekevent.setAlarms_(*args, **kwargs)
    
    def set_all_alarms_set_(self, *args, **kwargs):
        return self._ekevent.setAllAlarmsSet_(*args, **kwargs)
    
    def set_all_alarms_(self, *args, **kwargs):
        return self._ekevent.setAllAlarms_(*args, **kwargs)
    
    def set_all_day_(self, *args, **kwargs):
        return self._ekevent.setAllDay_(*args, **kwargs)
    
    def set_all_day_(self, *args, **kwargs):
        return self._ekevent.setAllDay_(*args, **kwargs)
    
    def set_app_link_(self, *args, **kwargs):
        return self._ekevent.setAppLink_(*args, **kwargs)
    
    def set_attachments_set_(self, *args, **kwargs):
        return self._ekevent.setAttachmentsSet_(*args, **kwargs)
    
    def set_attachments_(self, *args, **kwargs):
        return self._ekevent.setAttachments_(*args, **kwargs)
    
    def set_attendee_comment_(self, *args, **kwargs):
        return self._ekevent.setAttendeeComment_(*args, **kwargs)
    
    def set_attendee_declined_start_date_(self, *args, **kwargs):
        return self._ekevent.setAttendeeDeclinedStartDate_(*args, **kwargs)
    
    def set_attendee_proposed_start_date_(self, *args, **kwargs):
        return self._ekevent.setAttendeeProposedStartDate_(*args, **kwargs)
    
    def set_attendee_status_(self, *args, **kwargs):
        return self._ekevent.setAttendeeStatus_(*args, **kwargs)
    
    def set_attendees_raw_(self, *args, **kwargs):
        return self._ekevent.setAttendeesRaw_(*args, **kwargs)
    
    def set_attendees_(self, *args, **kwargs):
        return self._ekevent.setAttendees_(*args, **kwargs)
    
    def set_availability_(self, *args, **kwargs):
        return self._ekevent.setAvailability_(*args, **kwargs)
    
    def set_backing_object_(self, *args, **kwargs):
        return self._ekevent.setBackingObject_(*args, **kwargs)
    
    def set_birthday_contact_identifier_(self, *args, **kwargs):
        return self._ekevent.setBirthdayContactIdentifier_(*args, **kwargs)
    
    def set_birthday_contact_(self, *args, **kwargs):
        return self._ekevent.setBirthdayContact_(*args, **kwargs)
    
    def set_cached_junk_status_(self, *args, **kwargs):
        return self._ekevent.setCachedJunkStatus_(*args, **kwargs)
    
    def set_cached_melted_object_for_single_value_key_(self, *args, **kwargs):
        return self._ekevent.setCachedMeltedObject_forSingleValueKey_(*args, **kwargs)
    
    def set_cached_melted_objects_(self, *args, **kwargs):
        return self._ekevent.setCachedMeltedObjects_(*args, **kwargs)
    
    def set_cached_melted_objects_(self, *args, **kwargs):
        return self._ekevent.setCachedMeltedObjects_(*args, **kwargs)
    
    def set_cached_melted_objects_for_multi_value_key_(self, *args, **kwargs):
        return self._ekevent.setCachedMeltedObjects_forMultiValueKey_(*args, **kwargs)
    
    def set_cached_value_for_key_(self, *args, **kwargs):
        return self._ekevent.setCachedValue_forKey_(*args, **kwargs)
    
    def set_calendar_item_identifier_(self, *args, **kwargs):
        return self._ekevent.setCalendarItemIdentifier_(*args, **kwargs)
    
    def set_calendar_scale_(self, *args, **kwargs):
        return self._ekevent.setCalendarScale_(*args, **kwargs)
    
    def set_calendar_(self, *args, **kwargs):
        return self._ekevent.setCalendar_(*args, **kwargs)
    
    def set_calendar_(self, *args, **kwargs):
        return self._ekevent.setCalendar_(*args, **kwargs)
    
    def set_change_set_(self, *args, **kwargs):
        return self._ekevent.setChangeSet_(*args, **kwargs)
    
    def set_clear_modified_flags_(self, *args, **kwargs):
        return self._ekevent.setClearModifiedFlags_(*args, **kwargs)
    
    def set_client_location_(self, *args, **kwargs):
        return self._ekevent.setClientLocation_(*args, **kwargs)
    
    def set_completed_(self, *args, **kwargs):
        return self._ekevent.setCompleted_(*args, **kwargs)
    
    def set_conference_u_r_l_string_(self, *args, **kwargs):
        return self._ekevent.setConferenceURLString_(*args, **kwargs)
    
    def set_conference_u_r_l_(self, *args, **kwargs):
        return self._ekevent.setConferenceURL_(*args, **kwargs)
    
    def set_creation_date_(self, *args, **kwargs):
        return self._ekevent.setCreationDate_(*args, **kwargs)
    
    def set_custom_object_for_key_(self, *args, **kwargs):
        return self._ekevent.setCustomObject_forKey_(*args, **kwargs)
    
    def set_date_changed_(self, *args, **kwargs):
        return self._ekevent.setDateChanged_(*args, **kwargs)
    
    def set_default_alarm_was_deleted_(self, *args, **kwargs):
        return self._ekevent.setDefaultAlarmWasDeleted_(*args, **kwargs)
    
    def set_detached_items_(self, *args, **kwargs):
        return self._ekevent.setDetachedItems_(*args, **kwargs)
    
    def set_display_notes_(self, *args, **kwargs):
        return self._ekevent.setDisplayNotes_(*args, **kwargs)
    
    def set_display_notes_(self, *args, **kwargs):
        return self._ekevent.setDisplayNotes_(*args, **kwargs)
    
    def set_ek_exception_dates_(self, *args, **kwargs):
        return self._ekevent.setEkExceptionDates_(*args, **kwargs)
    
    def set_end_date_raw_(self, *args, **kwargs):
        return self._ekevent.setEndDateRaw_(*args, **kwargs)
    
    def set_end_date_unadjusted_for_legacy_clients_(self, *args, **kwargs):
        return self._ekevent.setEndDateUnadjustedForLegacyClients_(*args, **kwargs)
    
    def set_end_date_(self, *args, **kwargs):
        return self._ekevent.setEndDate_(*args, **kwargs)
    
    def set_end_location_(self, *args, **kwargs):
        return self._ekevent.setEndLocation_(*args, **kwargs)
    
    def set_end_time_zone_name_(self, *args, **kwargs):
        return self._ekevent.setEndTimeZoneName_(*args, **kwargs)
    
    def set_end_time_zone_(self, *args, **kwargs):
        return self._ekevent.setEndTimeZone_(*args, **kwargs)
    
    def set_event_store_(self, *args, **kwargs):
        return self._ekevent.setEventStore_(*args, **kwargs)
    
    def set_exception_dates_(self, *args, **kwargs):
        return self._ekevent.setExceptionDates_(*args, **kwargs)
    
    def set_external_data_(self, *args, **kwargs):
        return self._ekevent.setExternalData_(*args, **kwargs)
    
    def set_external_i_d_(self, *args, **kwargs):
        return self._ekevent.setExternalID_(*args, **kwargs)
    
    def set_external_modification_tag_(self, *args, **kwargs):
        return self._ekevent.setExternalModificationTag_(*args, **kwargs)
    
    def set_external_schedule_i_d_(self, *args, **kwargs):
        return self._ekevent.setExternalScheduleID_(*args, **kwargs)
    
    def set_external_tracking_status_(self, *args, **kwargs):
        return self._ekevent.setExternalTrackingStatus_(*args, **kwargs)
    
    def set_fired_t_t_l_(self, *args, **kwargs):
        return self._ekevent.setFiredTTL_(*args, **kwargs)
    
    def set_flag_value_(self, *args, **kwargs):
        return self._ekevent.setFlag_value_(*args, **kwargs)
    
    def set_flags_(self, *args, **kwargs):
        return self._ekevent.setFlags_(*args, **kwargs)
    
    def set_image_(self, *args, **kwargs):
        return self._ekevent.setImage_(*args, **kwargs)
    
    def set_invitation_changed_properties_(self, *args, **kwargs):
        return self._ekevent.setInvitationChangedProperties_(*args, **kwargs)
    
    def set_invitation_status_(self, *args, **kwargs):
        return self._ekevent.setInvitationStatus_(*args, **kwargs)
    
    def set_is_alerted_(self, *args, **kwargs):
        return self._ekevent.setIsAlerted_(*args, **kwargs)
    
    def set_is_junk_should_save_(self, *args, **kwargs):
        return self._ekevent.setIsJunk_shouldSave_(*args, **kwargs)
    
    def set_is_phantom_(self, *args, **kwargs):
        return self._ekevent.setIsPhantom_(*args, **kwargs)
    
    def set_junk_status_(self, *args, **kwargs):
        return self._ekevent.setJunkStatus_(*args, **kwargs)
    
    def set_last_modified_date_(self, *args, **kwargs):
        return self._ekevent.setLastModifiedDate_(*args, **kwargs)
    
    def set_local_custom_object_for_key_(self, *args, **kwargs):
        return self._ekevent.setLocalCustomObject_forKey_(*args, **kwargs)
    
    def set_local_structured_data_(self, *args, **kwargs):
        return self._ekevent.setLocalStructuredData_(*args, **kwargs)
    
    def set_location_changed_(self, *args, **kwargs):
        return self._ekevent.setLocationChanged_(*args, **kwargs)
    
    def set_location_prediction_allowed_(self, *args, **kwargs):
        return self._ekevent.setLocationPredictionAllowed_(*args, **kwargs)
    
    def set_location_prediction_state_(self, *args, **kwargs):
        return self._ekevent.setLocationPredictionState_(*args, **kwargs)
    
    def set_location_(self, *args, **kwargs):
        return self._ekevent.setLocation_(*args, **kwargs)
    
    def set_locations_(self, *args, **kwargs):
        return self._ekevent.setLocations_(*args, **kwargs)
    
    def set_lunar_calendar_string_(self, *args, **kwargs):
        return self._ekevent.setLunarCalendarString_(*args, **kwargs)
    
    def set_modified_properties_(self, *args, **kwargs):
        return self._ekevent.setModifiedProperties_(*args, **kwargs)
    
    def set_needs_geocoding_(self, *args, **kwargs):
        return self._ekevent.setNeedsGeocoding_(*args, **kwargs)
    
    def set_nil_value_for_key_(self, *args, **kwargs):
        return self._ekevent.setNilValueForKey_(*args, **kwargs)
    
    def set_notes_common_(self, *args, **kwargs):
        return self._ekevent.setNotesCommon_(*args, **kwargs)
    
    def set_notes_(self, *args, **kwargs):
        return self._ekevent.setNotes_(*args, **kwargs)
    
    def set_notes_(self, *args, **kwargs):
        return self._ekevent.setNotes_(*args, **kwargs)
    
    def set_observation_info_(self, *args, **kwargs):
        return self._ekevent.setObservationInfo_(*args, **kwargs)
    
    def set_observation_for_observing_key_path_(self, *args, **kwargs):
        return self._ekevent.setObservation_forObservingKeyPath_(*args, **kwargs)
    
    def set_occurrence_end_date_(self, *args, **kwargs):
        return self._ekevent.setOccurrenceEndDate_(*args, **kwargs)
    
    def set_occurrence_is_all_day_(self, *args, **kwargs):
        return self._ekevent.setOccurrenceIsAllDay_(*args, **kwargs)
    
    def set_occurrence_start_date_(self, *args, **kwargs):
        return self._ekevent.setOccurrenceStartDate_(*args, **kwargs)
    
    def set_organizer_(self, *args, **kwargs):
        return self._ekevent.setOrganizer_(*args, **kwargs)
    
    def set_original_item_(self, *args, **kwargs):
        return self._ekevent.setOriginalItem_(*args, **kwargs)
    
    def set_original_occurrence_end_date_(self, *args, **kwargs):
        return self._ekevent.setOriginalOccurrenceEndDate_(*args, **kwargs)
    
    def set_original_occurrence_is_all_day_(self, *args, **kwargs):
        return self._ekevent.setOriginalOccurrenceIsAllDay_(*args, **kwargs)
    
    def set_original_occurrence_start_date_(self, *args, **kwargs):
        return self._ekevent.setOriginalOccurrenceStartDate_(*args, **kwargs)
    
    def set_original_start_date_(self, *args, **kwargs):
        return self._ekevent.setOriginalStartDate_(*args, **kwargs)
    
    def set_participation_status_modified_date_(self, *args, **kwargs):
        return self._ekevent.setParticipationStatusModifiedDate_(*args, **kwargs)
    
    def set_participation_status_(self, *args, **kwargs):
        return self._ekevent.setParticipationStatus_(*args, **kwargs)
    
    def set_persistent_object_(self, *args, **kwargs):
        return self._ekevent.setPersistentObject_(*args, **kwargs)
    
    def set_phantom_master_(self, *args, **kwargs):
        return self._ekevent.setPhantomMaster_(*args, **kwargs)
    
    def set_predicted_location_frozen_(self, *args, **kwargs):
        return self._ekevent.setPredictedLocationFrozen_(*args, **kwargs)
    
    def set_prevent_conference_u_r_l_detection_(self, *args, **kwargs):
        return self._ekevent.setPreventConferenceURLDetection_(*args, **kwargs)
    
    def set_priority_(self, *args, **kwargs):
        return self._ekevent.setPriority_(*args, **kwargs)
    
    def set_privacy_level_without_verifying_privacy_modifications_allowed_(self, *args, **kwargs):
        return self._ekevent.setPrivacyLevelWithoutVerifyingPrivacyModificationsAllowed_(*args, **kwargs)
    
    def set_privacy_level_(self, *args, **kwargs):
        return self._ekevent.setPrivacyLevel_(*args, **kwargs)
    
    def set_proposed_start_date_(self, *args, **kwargs):
        return self._ekevent.setProposedStartDate_(*args, **kwargs)
    
    def set_recurrence_changed_(self, *args, **kwargs):
        return self._ekevent.setRecurrenceChanged_(*args, **kwargs)
    
    def set_recurrence_rule_string_(self, *args, **kwargs):
        return self._ekevent.setRecurrenceRuleString_(*args, **kwargs)
    
    def set_recurrence_rule_(self, *args, **kwargs):
        return self._ekevent.setRecurrenceRule_(*args, **kwargs)
    
    def set_recurrence_rules_set_(self, *args, **kwargs):
        return self._ekevent.setRecurrenceRulesSet_(*args, **kwargs)
    
    def set_recurrence_rules_(self, *args, **kwargs):
        return self._ekevent.setRecurrenceRules_(*args, **kwargs)
    
    def set_recurrence_set_(self, *args, **kwargs):
        return self._ekevent.setRecurrenceSet_(*args, **kwargs)
    
    def set_requires_detach_due_to_snoozed_alarm_(self, *args, **kwargs):
        return self._ekevent.setRequiresDetachDueToSnoozedAlarm_(*args, **kwargs)
    
    def set_response_comment_(self, *args, **kwargs):
        return self._ekevent.setResponseComment_(*args, **kwargs)
    
    def set_scripting_properties_(self, *args, **kwargs):
        return self._ekevent.setScriptingProperties_(*args, **kwargs)
    
    def set_self_attendee_(self, *args, **kwargs):
        return self._ekevent.setSelfAttendee_(*args, **kwargs)
    
    def set_sequence_number_(self, *args, **kwargs):
        return self._ekevent.setSequenceNumber_(*args, **kwargs)
    
    def set_shared_item_created_by_address_string_(self, *args, **kwargs):
        return self._ekevent.setSharedItemCreatedByAddressString_(*args, **kwargs)
    
    def set_shared_item_created_by_address_(self, *args, **kwargs):
        return self._ekevent.setSharedItemCreatedByAddress_(*args, **kwargs)
    
    def set_shared_item_created_by_display_name_(self, *args, **kwargs):
        return self._ekevent.setSharedItemCreatedByDisplayName_(*args, **kwargs)
    
    def set_shared_item_created_by_first_name_(self, *args, **kwargs):
        return self._ekevent.setSharedItemCreatedByFirstName_(*args, **kwargs)
    
    def set_shared_item_created_by_last_name_(self, *args, **kwargs):
        return self._ekevent.setSharedItemCreatedByLastName_(*args, **kwargs)
    
    def set_shared_item_created_date_(self, *args, **kwargs):
        return self._ekevent.setSharedItemCreatedDate_(*args, **kwargs)
    
    def set_shared_item_created_time_zone_name_(self, *args, **kwargs):
        return self._ekevent.setSharedItemCreatedTimeZoneName_(*args, **kwargs)
    
    def set_shared_item_created_time_zone_(self, *args, **kwargs):
        return self._ekevent.setSharedItemCreatedTimeZone_(*args, **kwargs)
    
    def set_shared_item_modified_by_address_string_(self, *args, **kwargs):
        return self._ekevent.setSharedItemModifiedByAddressString_(*args, **kwargs)
    
    def set_shared_item_modified_by_address_(self, *args, **kwargs):
        return self._ekevent.setSharedItemModifiedByAddress_(*args, **kwargs)
    
    def set_shared_item_modified_by_display_name_(self, *args, **kwargs):
        return self._ekevent.setSharedItemModifiedByDisplayName_(*args, **kwargs)
    
    def set_shared_item_modified_by_first_name_(self, *args, **kwargs):
        return self._ekevent.setSharedItemModifiedByFirstName_(*args, **kwargs)
    
    def set_shared_item_modified_by_last_name_(self, *args, **kwargs):
        return self._ekevent.setSharedItemModifiedByLastName_(*args, **kwargs)
    
    def set_shared_item_modified_date_(self, *args, **kwargs):
        return self._ekevent.setSharedItemModifiedDate_(*args, **kwargs)
    
    def set_shared_item_modified_time_zone_name_(self, *args, **kwargs):
        return self._ekevent.setSharedItemModifiedTimeZoneName_(*args, **kwargs)
    
    def set_shared_item_modified_time_zone_(self, *args, **kwargs):
        return self._ekevent.setSharedItemModifiedTimeZone_(*args, **kwargs)
    
    def set_single_changed_value_for_key_(self, *args, **kwargs):
        return self._ekevent.setSingleChangedValue_forKey_(*args, **kwargs)
    
    def set_single_recurrence_rule_(self, *args, **kwargs):
        return self._ekevent.setSingleRecurrenceRule_(*args, **kwargs)
    
    def set_special_day_string_(self, *args, **kwargs):
        return self._ekevent.setSpecialDayString_(*args, **kwargs)
    
    def set_special_day_type_(self, *args, **kwargs):
        return self._ekevent.setSpecialDayType_(*args, **kwargs)
    
    def set_start_date_raw_(self, *args, **kwargs):
        return self._ekevent.setStartDateRaw_(*args, **kwargs)
    
    def set_start_date_raw_(self, *args, **kwargs):
        return self._ekevent.setStartDateRaw_(*args, **kwargs)
    
    def set_start_date_(self, *args, **kwargs):
        return self._ekevent.setStartDate_(*args, **kwargs)
    
    def set_start_time_zone_name_(self, *args, **kwargs):
        return self._ekevent.setStartTimeZoneName_(*args, **kwargs)
    
    def set_start_time_zone_(self, *args, **kwargs):
        return self._ekevent.setStartTimeZone_(*args, **kwargs)
    
    def set_status_(self, *args, **kwargs):
        return self._ekevent.setStatus_(*args, **kwargs)
    
    def set_structured_data_(self, *args, **kwargs):
        return self._ekevent.setStructuredData_(*args, **kwargs)
    
    def set_structured_location_without_prediction_(self, *args, **kwargs):
        return self._ekevent.setStructuredLocationWithoutPrediction_(*args, **kwargs)
    
    def set_structured_location_(self, *args, **kwargs):
        return self._ekevent.setStructuredLocation_(*args, **kwargs)
    
    def set_structured_location_(self, *args, **kwargs):
        return self._ekevent.setStructuredLocation_(*args, **kwargs)
    
    def set_structured_location_preserve_conference_rooms_(self, *args, **kwargs):
        return self._ekevent.setStructuredLocation_preserveConferenceRooms_(*args, **kwargs)
    
    def set_suggestion_info_(self, *args, **kwargs):
        return self._ekevent.setSuggestionInfo_(*args, **kwargs)
    
    def set_suppress_notification_for_changes_(self, *args, **kwargs):
        return self._ekevent.setSuppressNotificationForChanges_(*args, **kwargs)
    
    def set_sync_error_(self, *args, **kwargs):
        return self._ekevent.setSyncError_(*args, **kwargs)
    
    def set_time_changed_(self, *args, **kwargs):
        return self._ekevent.setTimeChanged_(*args, **kwargs)
    
    def set_time_zone_(self, *args, **kwargs):
        return self._ekevent.setTimeZone_(*args, **kwargs)
    
    def set_time_zone_(self, *args, **kwargs):
        return self._ekevent.setTimeZone_(*args, **kwargs)
    
    def set_title_changed_(self, *args, **kwargs):
        return self._ekevent.setTitleChanged_(*args, **kwargs)
    
    def set_title_(self, *args, **kwargs):
        return self._ekevent.setTitle_(*args, **kwargs)
    
    def set_title_(self, *args, **kwargs):
        return self._ekevent.setTitle_(*args, **kwargs)
    
    def set_travel_advisory_behavior_(self, *args, **kwargs):
        return self._ekevent.setTravelAdvisoryBehavior_(*args, **kwargs)
    
    def set_travel_start_location_(self, *args, **kwargs):
        return self._ekevent.setTravelStartLocation_(*args, **kwargs)
    
    def set_travel_time_(self, *args, **kwargs):
        return self._ekevent.setTravelTime_(*args, **kwargs)
    
    def set_u_r_l_common_(self, *args, **kwargs):
        return self._ekevent.setURLCommon_(*args, **kwargs)
    
    def set_u_r_l_string_(self, *args, **kwargs):
        return self._ekevent.setURLString_(*args, **kwargs)
    
    def set_u_r_l_(self, *args, **kwargs):
        return self._ekevent.setURL_(*args, **kwargs)
    
    def set_u_r_l_(self, *args, **kwargs):
        return self._ekevent.setURL_(*args, **kwargs)
    
    def set_unique_i_d_(self, *args, **kwargs):
        return self._ekevent.setUniqueID_(*args, **kwargs)
    
    def set_unique_id_(self, *args, **kwargs):
        return self._ekevent.setUniqueId_(*args, **kwargs)
    
    def set_unlocalized_title_(self, *args, **kwargs):
        return self._ekevent.setUnlocalizedTitle_(*args, **kwargs)
    
    def set_user_interface_item_identifier_(self, *args, **kwargs):
        return self._ekevent.setUserInterfaceItemIdentifier_(*args, **kwargs)
    
    def set_value_for_key_path_(self, *args, **kwargs):
        return self._ekevent.setValue_forKeyPath_(*args, **kwargs)
    
    def set_value_for_key_(self, *args, **kwargs):
        return self._ekevent.setValue_forKey_(*args, **kwargs)
    
    def set_value_for_undefined_key_(self, *args, **kwargs):
        return self._ekevent.setValue_forUndefinedKey_(*args, **kwargs)
    
    def set_values_for_keys_with_dictionary_(self, *args, **kwargs):
        return self._ekevent.setValuesForKeysWithDictionary_(*args, **kwargs)
    
    def set_video_conference_changed_(self, *args, **kwargs):
        return self._ekevent.setVideoConferenceChanged_(*args, **kwargs)
    
    def set_virtual_conference_text_representation_(self, *args, **kwargs):
        return self._ekevent.setVirtualConferenceTextRepresentation_(*args, **kwargs)
    
    def set_virtual_conference_(self, *args, **kwargs):
        return self._ekevent.setVirtualConference_(*args, **kwargs)
    
    def set_cached_melted_objects_(self, *args, **kwargs):
        return self._ekevent.set_cachedMeltedObjects_(*args, **kwargs)
    
    def set_cached_values_(self, *args, **kwargs):
        return self._ekevent.set_cachedValues_(*args, **kwargs)
    
    def set_validation_context_(self, *args, **kwargs):
        return self._ekevent.set_validationContext_(*args, **kwargs)
    
    def shallow_copy_without_changes(self, *args, **kwargs):
        return self._ekevent.shallowCopyWithoutChanges(*args, **kwargs)
    
    def shared_item_created_by_address(self, *args, **kwargs):
        return self._ekevent.sharedItemCreatedByAddress(*args, **kwargs)
    
    def shared_item_created_by_address_string(self, *args, **kwargs):
        return self._ekevent.sharedItemCreatedByAddressString(*args, **kwargs)
    
    def shared_item_created_by_display_name(self, *args, **kwargs):
        return self._ekevent.sharedItemCreatedByDisplayName(*args, **kwargs)
    
    def shared_item_created_by_first_name(self, *args, **kwargs):
        return self._ekevent.sharedItemCreatedByFirstName(*args, **kwargs)
    
    def shared_item_created_by_last_name(self, *args, **kwargs):
        return self._ekevent.sharedItemCreatedByLastName(*args, **kwargs)
    
    def shared_item_created_date(self, *args, **kwargs):
        return self._ekevent.sharedItemCreatedDate(*args, **kwargs)
    
    def shared_item_created_time_zone(self, *args, **kwargs):
        return self._ekevent.sharedItemCreatedTimeZone(*args, **kwargs)
    
    def shared_item_created_time_zone_name(self, *args, **kwargs):
        return self._ekevent.sharedItemCreatedTimeZoneName(*args, **kwargs)
    
    def shared_item_modified_by_address(self, *args, **kwargs):
        return self._ekevent.sharedItemModifiedByAddress(*args, **kwargs)
    
    def shared_item_modified_by_address_string(self, *args, **kwargs):
        return self._ekevent.sharedItemModifiedByAddressString(*args, **kwargs)
    
    def shared_item_modified_by_display_name(self, *args, **kwargs):
        return self._ekevent.sharedItemModifiedByDisplayName(*args, **kwargs)
    
    def shared_item_modified_by_first_name(self, *args, **kwargs):
        return self._ekevent.sharedItemModifiedByFirstName(*args, **kwargs)
    
    def shared_item_modified_by_last_name(self, *args, **kwargs):
        return self._ekevent.sharedItemModifiedByLastName(*args, **kwargs)
    
    def shared_item_modified_date(self, *args, **kwargs):
        return self._ekevent.sharedItemModifiedDate(*args, **kwargs)
    
    def shared_item_modified_time_zone(self, *args, **kwargs):
        return self._ekevent.sharedItemModifiedTimeZone(*args, **kwargs)
    
    def shared_item_modified_time_zone_name(self, *args, **kwargs):
        return self._ekevent.sharedItemModifiedTimeZoneName(*args, **kwargs)
    
    def shared_u_i_d(self, *args, **kwargs):
        return self._ekevent.sharedUID(*args, **kwargs)
    
    def should_have_default_alarms(self, *args, **kwargs):
        return self._ekevent.shouldHaveDefaultAlarms(*args, **kwargs)
    
    def should_have_default_alarms(self, *args, **kwargs):
        return self._ekevent.shouldHaveDefaultAlarms(*args, **kwargs)
    
    def should_load_relationship_for_validation_(self, *args, **kwargs):
        return self._ekevent.shouldLoadRelationshipForValidation_(*args, **kwargs)
    
    def should_load_relationship_for_validation_(self, *args, **kwargs):
        return self._ekevent.shouldLoadRelationshipForValidation_(*args, **kwargs)
    
    def show_event_u_r_l_string(self, *args, **kwargs):
        return self._ekevent.showEventURLString(*args, **kwargs)
    
    def single_changed_value_for_key_(self, *args, **kwargs):
        return self._ekevent.singleChangedValueForKey_(*args, **kwargs)
    
    def single_recurrence_rule(self, *args, **kwargs):
        return self._ekevent.singleRecurrenceRule(*args, **kwargs)
    
    def snapshot_copy(self, *args, **kwargs):
        return self._ekevent.snapshotCopy(*args, **kwargs)
    
    def snapshot_copy_with_property_keys_to_copy_(self, *args, **kwargs):
        return self._ekevent.snapshotCopyWithPropertyKeysToCopy_(*args, **kwargs)
    
    def snapshot_copy_with_property_keys_to_copy_property_keys_to_skip_(self, *args, **kwargs):
        return self._ekevent.snapshotCopyWithPropertyKeysToCopy_propertyKeysToSkip_(*args, **kwargs)
    
    def snapshot_copy_with_property_keys_to_copy_property_keys_to_skip_(self, *args, **kwargs):
        return self._ekevent.snapshotCopyWithPropertyKeysToCopy_propertyKeysToSkip_(*args, **kwargs)
    
    def snooze_alarm_until_target_date_(self, *args, **kwargs):
        return self._ekevent.snoozeAlarm_untilTargetDate_(*args, **kwargs)
    
    def snooze_alarm_until_target_date_pins_trigger_to_start_date_(self, *args, **kwargs):
        return self._ekevent.snoozeAlarm_untilTargetDate_pinsTriggerToStartDate_(*args, **kwargs)
    
    def snooze_alarm_with_location_proximity_(self, *args, **kwargs):
        return self._ekevent.snoozeAlarm_withLocation_proximity_(*args, **kwargs)
    
    def snooze_alarm_with_time_interval_from_now_(self, *args, **kwargs):
        return self._ekevent.snoozeAlarm_withTimeIntervalFromNow_(*args, **kwargs)
    
    def snooze_alarm_with_time_interval_from_now_(self, *args, **kwargs):
        return self._ekevent.snoozeAlarm_withTimeIntervalFromNow_(*args, **kwargs)
    
    def snooze_alarm_with_time_interval_from_now_pins_trigger_to_start_date_(self, *args, **kwargs):
        return self._ekevent.snoozeAlarm_withTimeIntervalFromNow_pinsTriggerToStartDate_(*args, **kwargs)
    
    def snooze_alarm_with_time_interval_from_now_pins_trigger_to_start_date_(self, *args, **kwargs):
        return self._ekevent.snoozeAlarm_withTimeIntervalFromNow_pinsTriggerToStartDate_(*args, **kwargs)
    
    def sorted_alarms(self, *args, **kwargs):
        return self._ekevent.sortedAlarms(*args, **kwargs)
    
    def special_day_string(self, *args, **kwargs):
        return self._ekevent.specialDayString(*args, **kwargs)
    
    def special_day_type(self, *args, **kwargs):
        return self._ekevent.specialDayType(*args, **kwargs)
    
    def specific_identifier(self, *args, **kwargs):
        return self._ekevent.specificIdentifier(*args, **kwargs)
    
    def specific_identifier(self, *args, **kwargs):
        return self._ekevent.specificIdentifier(*args, **kwargs)
    
    def start_calendar_date(self, *args, **kwargs):
        return self._ekevent.startCalendarDate(*args, **kwargs)
    
    def start_calendar_date_including_travel_time(self, *args, **kwargs):
        return self._ekevent.startCalendarDateIncludingTravelTime(*args, **kwargs)
    
    def start_date(self, *args, **kwargs):
        return self._ekevent.startDate(*args, **kwargs)
    
    def start_date_for_recurrence(self, *args, **kwargs):
        return self._ekevent.startDateForRecurrence(*args, **kwargs)
    
    def start_date_for_recurrence(self, *args, **kwargs):
        return self._ekevent.startDateForRecurrence(*args, **kwargs)
    
    def start_date_including_travel(self, *args, **kwargs):
        return self._ekevent.startDateIncludingTravel(*args, **kwargs)
    
    def start_date_raw(self, *args, **kwargs):
        return self._ekevent.startDateRaw(*args, **kwargs)
    
    def start_date_raw(self, *args, **kwargs):
        return self._ekevent.startDateRaw(*args, **kwargs)
    
    def start_of_day_for_end_date_in_calendar_(self, *args, **kwargs):
        return self._ekevent.startOfDayForEndDateInCalendar_(*args, **kwargs)
    
    def start_of_day_for_start_date_in_calendar_(self, *args, **kwargs):
        return self._ekevent.startOfDayForStartDateInCalendar_(*args, **kwargs)
    
    def start_time_zone(self, *args, **kwargs):
        return self._ekevent.startTimeZone(*args, **kwargs)
    
    def start_time_zone_name(self, *args, **kwargs):
        return self._ekevent.startTimeZoneName(*args, **kwargs)
    
    def status(self, *args, **kwargs):
        return self._ekevent.status(*args, **kwargs)
    
    def stored_value_for_key_(self, *args, **kwargs):
        return self._ekevent.storedValueForKey_(*args, **kwargs)
    
    def string_value_safe(self, *args, **kwargs):
        return self._ekevent.stringValueSafe(*args, **kwargs)
    
    def string_value_safe_(self, *args, **kwargs):
        return self._ekevent.stringValueSafe_(*args, **kwargs)
    
    def structured_data(self, *args, **kwargs):
        return self._ekevent.structuredData(*args, **kwargs)
    
    def structured_location(self, *args, **kwargs):
        return self._ekevent.structuredLocation(*args, **kwargs)
    
    def structured_location(self, *args, **kwargs):
        return self._ekevent.structuredLocation(*args, **kwargs)
    
    def structured_location_without_prediction(self, *args, **kwargs):
        return self._ekevent.structuredLocationWithoutPrediction(*args, **kwargs)
    
    def suggested_start_date_for_current_recurrence_rule(self, *args, **kwargs):
        return self._ekevent.suggestedStartDateForCurrentRecurrenceRule(*args, **kwargs)
    
    def suggested_start_date_for_current_recurrence_rule_with_simulated_now_date_(self, *args, **kwargs):
        return self._ekevent.suggestedStartDateForCurrentRecurrenceRuleWithSimulatedNowDate_(*args, **kwargs)
    
    def suggestion_info(self, *args, **kwargs):
        return self._ekevent.suggestionInfo(*args, **kwargs)
    
    def superclass(self, *args, **kwargs):
        return self._ekevent.superclass(*args, **kwargs)
    
    def supports_adding_attachments(self, *args, **kwargs):
        return self._ekevent.supportsAddingAttachments(*args, **kwargs)
    
    def supports_b_s_x_p_c_secure_coding(self, *args, **kwargs):
        return self._ekevent.supportsBSXPCSecureCoding(*args, **kwargs)
    
    def supports_junk_reporting(self, *args, **kwargs):
        return self._ekevent.supportsJunkReporting(*args, **kwargs)
    
    def supports_participation_status_modifications_without_notification(self, *args, **kwargs):
        return self._ekevent.supportsParticipationStatusModificationsWithoutNotification(*args, **kwargs)
    
    def supports_r_b_s_x_p_c_secure_coding(self, *args, **kwargs):
        return self._ekevent.supportsRBSXPCSecureCoding(*args, **kwargs)
    
    def suppress_notification_for_changes(self, *args, **kwargs):
        return self._ekevent.suppressNotificationForChanges(*args, **kwargs)
    
    def sync_error(self, *args, **kwargs):
        return self._ekevent.syncError(*args, **kwargs)
    
    def take_stored_value_for_key_(self, *args, **kwargs):
        return self._ekevent.takeStoredValue_forKey_(*args, **kwargs)
    
    def take_stored_values_from_dictionary_(self, *args, **kwargs):
        return self._ekevent.takeStoredValuesFromDictionary_(*args, **kwargs)
    
    def take_value_for_key_path_(self, *args, **kwargs):
        return self._ekevent.takeValue_forKeyPath_(*args, **kwargs)
    
    def take_value_for_key_(self, *args, **kwargs):
        return self._ekevent.takeValue_forKey_(*args, **kwargs)
    
    def take_values_from_dictionary_(self, *args, **kwargs):
        return self._ekevent.takeValuesFromDictionary_(*args, **kwargs)
    
    def time_changed(self, *args, **kwargs):
        return self._ekevent.timeChanged(*args, **kwargs)
    
    def time_zone(self, *args, **kwargs):
        return self._ekevent.timeZone(*args, **kwargs)
    
    def title(self, *args, **kwargs):
        return self._ekevent.title(*args, **kwargs)
    
    def title(self, *args, **kwargs):
        return self._ekevent.title(*args, **kwargs)
    
    def title_changed(self, *args, **kwargs):
        return self._ekevent.titleChanged(*args, **kwargs)
    
    def to_many_relationship_keys(self, *args, **kwargs):
        return self._ekevent.toManyRelationshipKeys(*args, **kwargs)
    
    def to_one_relationship_keys(self, *args, **kwargs):
        return self._ekevent.toOneRelationshipKeys(*args, **kwargs)
    
    def to_p_b_codable(self, *args, **kwargs):
        return self._ekevent.toPBCodable(*args, **kwargs)
    
    def travel_advisory_behavior(self, *args, **kwargs):
        return self._ekevent.travelAdvisoryBehavior(*args, **kwargs)
    
    def travel_advisory_behavior_is_effectively_enabled(self, *args, **kwargs):
        return self._ekevent.travelAdvisoryBehaviorIsEffectivelyEnabled(*args, **kwargs)
    
    def travel_routing_mode(self, *args, **kwargs):
        return self._ekevent.travelRoutingMode(*args, **kwargs)
    
    def travel_start_location(self, *args, **kwargs):
        return self._ekevent.travelStartLocation(*args, **kwargs)
    
    def travel_time(self, *args, **kwargs):
        return self._ekevent.travelTime(*args, **kwargs)
    
    def un_safe_bool_value(self, *args, **kwargs):
        return self._ekevent.un_safeBoolValue(*args, **kwargs)
    
    def unable_to_set_nil_for_key_(self, *args, **kwargs):
        return self._ekevent.unableToSetNilForKey_(*args, **kwargs)
    
    def unbind_(self, *args, **kwargs):
        return self._ekevent.unbind_(*args, **kwargs)
    
    def unique_i_d(self, *args, **kwargs):
        return self._ekevent.uniqueID(*args, **kwargs)
    
    def unique_id(self, *args, **kwargs):
        return self._ekevent.uniqueId(*args, **kwargs)
    
    def unique_id(self, *args, **kwargs):
        return self._ekevent.uniqueId(*args, **kwargs)
    
    def unique_identifier(self, *args, **kwargs):
        return self._ekevent.uniqueIdentifier(*args, **kwargs)
    
    def unlocalized_title(self, *args, **kwargs):
        return self._ekevent.unlocalizedTitle(*args, **kwargs)
    
    def update_after_applying_changes_(self, *args, **kwargs):
        return self._ekevent.updateAfterApplyingChanges_(*args, **kwargs)
    
    def update_default_alarms(self, *args, **kwargs):
        return self._ekevent.updateDefaultAlarms(*args, **kwargs)
    
    def update_event_to_event_(self, *args, **kwargs):
        return self._ekevent.updateEventToEvent_(*args, **kwargs)
    
    def update_event_to_event_commit_(self, *args, **kwargs):
        return self._ekevent.updateEventToEvent_commit_(*args, **kwargs)
    
    def update_melted_and_cached_multi_relation_objects_for_key_(self, *args, **kwargs):
        return self._ekevent.updateMeltedAndCachedMultiRelationObjects_forKey_(*args, **kwargs)
    
    def update_melted_and_cached_single_relation_object_for_key_frozen_class_(self, *args, **kwargs):
        return self._ekevent.updateMeltedAndCachedSingleRelationObject_forKey_frozenClass_(*args, **kwargs)
    
    def update_melted_cache_for_change_set_(self, *args, **kwargs):
        return self._ekevent.updateMeltedCacheForChangeSet_(*args, **kwargs)
    
    def update_multi_value_cache_for_change_set_preserving_existing_adds_(self, *args, **kwargs):
        return self._ekevent.updateMultiValueCacheForChangeSet_preservingExistingAdds_(*args, **kwargs)
    
    def update_persistent_object(self, *args, **kwargs):
        return self._ekevent.updatePersistentObject(*args, **kwargs)
    
    def update_persistent_object_skipping_properties_(self, *args, **kwargs):
        return self._ekevent.updatePersistentObjectSkippingProperties_(*args, **kwargs)
    
    def update_persistent_value_for_key_if_needed_(self, *args, **kwargs):
        return self._ekevent.updatePersistentValueForKeyIfNeeded_(*args, **kwargs)
    
    def update_with_app_link_used_selected_text_(self, *args, **kwargs):
        return self._ekevent.updateWithAppLink_usedSelectedText_(*args, **kwargs)
    
    def update_with_geocoded_map_item_and_save_with_commit_event_store_error_(self, *args, **kwargs):
        return self._ekevent.updateWithGeocodedMapItemAndSaveWithCommit_eventStore_error_(*args, **kwargs)
    
    def update_with_v_c_s_entity_in_calendar_(self, *args, **kwargs):
        return self._ekevent.updateWithVCSEntity_inCalendar_(*args, **kwargs)
    
    def update_with_v_c_s_entity_in_calendar_(self, *args, **kwargs):
        return self._ekevent.updateWithVCSEntity_inCalendar_(*args, **kwargs)
    
    def user_interface_item_identifier(self, *args, **kwargs):
        return self._ekevent.userInterfaceItemIdentifier(*args, **kwargs)
    
    def utf8_value_safe(self, *args, **kwargs):
        return self._ekevent.utf8ValueSafe(*args, **kwargs)
    
    def utf8_value_safe_(self, *args, **kwargs):
        return self._ekevent.utf8ValueSafe_(*args, **kwargs)
    
    def validate_occurrence_date_still_matches_recurrence_rules(self, *args, **kwargs):
        return self._ekevent.validateOccurrenceDateStillMatchesRecurrenceRules(*args, **kwargs)
    
    def validate_recurrence_rule_error_(self, *args, **kwargs):
        return self._ekevent.validateRecurrenceRule_error_(*args, **kwargs)
    
    def validate_take_value_for_key_path_(self, *args, **kwargs):
        return self._ekevent.validateTakeValue_forKeyPath_(*args, **kwargs)
    
    def validate_value_for_key_path_error_(self, *args, **kwargs):
        return self._ekevent.validateValue_forKeyPath_error_(*args, **kwargs)
    
    def validate_value_for_key_(self, *args, **kwargs):
        return self._ekevent.validateValue_forKey_(*args, **kwargs)
    
    def validate_value_for_key_error_(self, *args, **kwargs):
        return self._ekevent.validateValue_forKey_error_(*args, **kwargs)
    
    def validate_with_owner_error_(self, *args, **kwargs):
        return self._ekevent.validateWithOwner_error_(*args, **kwargs)
    
    def validate_with_span_error_(self, *args, **kwargs):
        return self._ekevent.validateWithSpan_error_(*args, **kwargs)
    
    def validate_(self, *args, **kwargs):
        return self._ekevent.validate_(*args, **kwargs)
    
    def validate_(self, *args, **kwargs):
        return self._ekevent.validate_(*args, **kwargs)
    
    def validate_(self, *args, **kwargs):
        return self._ekevent.validate_(*args, **kwargs)
    
    def value_at_index_in_property_with_key_(self, *args, **kwargs):
        return self._ekevent.valueAtIndex_inPropertyWithKey_(*args, **kwargs)
    
    def value_class_for_binding_(self, *args, **kwargs):
        return self._ekevent.valueClassForBinding_(*args, **kwargs)
    
    def value_for_key_path_(self, *args, **kwargs):
        return self._ekevent.valueForKeyPath_(*args, **kwargs)
    
    def value_for_key_(self, *args, **kwargs):
        return self._ekevent.valueForKey_(*args, **kwargs)
    
    def value_for_undefined_key_(self, *args, **kwargs):
        return self._ekevent.valueForUndefinedKey_(*args, **kwargs)
    
    def value_with_name_in_property_with_key_(self, *args, **kwargs):
        return self._ekevent.valueWithName_inPropertyWithKey_(*args, **kwargs)
    
    def value_with_unique_i_d_in_property_with_key_(self, *args, **kwargs):
        return self._ekevent.valueWithUniqueID_inPropertyWithKey_(*args, **kwargs)
    
    def values_for_keys_(self, *args, **kwargs):
        return self._ekevent.valuesForKeys_(*args, **kwargs)
    
    def video_conference_changed(self, *args, **kwargs):
        return self._ekevent.videoConferenceChanged(*args, **kwargs)
    
    def virtual_conference(self, *args, **kwargs):
        return self._ekevent.virtualConference(*args, **kwargs)
    
    def virtual_conference_text_representation(self, *args, **kwargs):
        return self._ekevent.virtualConferenceTextRepresentation(*args, **kwargs)
    
    def will_change_value_for_key_(self, *args, **kwargs):
        return self._ekevent.willChangeValueForKey_(*args, **kwargs)
    
    def will_change_value_for_key_with_set_mutation_using_objects_(self, *args, **kwargs):
        return self._ekevent.willChangeValueForKey_withSetMutation_usingObjects_(*args, **kwargs)
    
    def will_change_values_at_indexes_for_key_(self, *args, **kwargs):
        return self._ekevent.willChange_valuesAtIndexes_forKey_(*args, **kwargs)
    
    def will_save(self, *args, **kwargs):
        return self._ekevent.willSave(*args, **kwargs)
    
    def zone(self, *args, **kwargs):
        return self._ekevent.zone(*args, **kwargs)
    