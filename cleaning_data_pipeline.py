import prepare_data as prep_data

prep_data.clear_cs_data('computer_science_synthetic_dataset.csv')
prep_data.clear_psy_data('Psychology-10K.json')
prep_data.clear_km_data('Критичне_Мислення')
# to translate the data 
prep_data.translate_json('KM_data/km_data.json', 'KM_data/translated_km_data.json')