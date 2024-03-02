class CreateDocuments < ActiveRecord::Migration[7.1]
  def change
    create_table :documents do |t|
      t.string :name
      t.text :content

      t.timestamps
    end
  end
end
