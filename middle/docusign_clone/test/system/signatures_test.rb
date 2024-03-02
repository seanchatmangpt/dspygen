require "application_system_test_case"

class SignaturesTest < ApplicationSystemTestCase
  setup do
    @signature = signatures(:one)
  end

  test "visiting the index" do
    visit signatures_url
    assert_selector "h1", text: "Signatures"
  end

  test "should create signature" do
    visit signatures_url
    click_on "New signature"

    fill_in "Document", with: @signature.document_id
    fill_in "User", with: @signature.user_id
    click_on "Create Signature"

    assert_text "Signature was successfully created"
    click_on "Back"
  end

  test "should update Signature" do
    visit signature_url(@signature)
    click_on "Edit this signature", match: :first

    fill_in "Document", with: @signature.document_id
    fill_in "User", with: @signature.user_id
    click_on "Update Signature"

    assert_text "Signature was successfully updated"
    click_on "Back"
  end

  test "should destroy Signature" do
    visit signature_url(@signature)
    click_on "Destroy this signature", match: :first

    assert_text "Signature was successfully destroyed"
  end
end
