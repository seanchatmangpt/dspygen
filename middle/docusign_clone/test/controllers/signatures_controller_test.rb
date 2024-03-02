require "test_helper"

class SignaturesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @signature = signatures(:one)
  end

  test "should get index" do
    get signatures_url
    assert_response :success
  end

  test "should get new" do
    get new_signature_url
    assert_response :success
  end

  test "should create signature" do
    assert_difference("Signature.count") do
      post signatures_url, params: { signature: { document_id: @signature.document_id, user_id: @signature.user_id } }
    end

    assert_redirected_to signature_url(Signature.last)
  end

  test "should show signature" do
    get signature_url(@signature)
    assert_response :success
  end

  test "should get edit" do
    get edit_signature_url(@signature)
    assert_response :success
  end

  test "should update signature" do
    patch signature_url(@signature), params: { signature: { document_id: @signature.document_id, user_id: @signature.user_id } }
    assert_redirected_to signature_url(@signature)
  end

  test "should destroy signature" do
    assert_difference("Signature.count", -1) do
      delete signature_url(@signature)
    end

    assert_redirected_to signatures_url
  end
end
