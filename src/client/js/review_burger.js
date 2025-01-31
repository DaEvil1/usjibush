import { createApp, ref, watch, onMounted, VueElement } from 'vue';

const app = createApp({
    delimiters: ['[[', ']]'],
    setup() {
        const formData = ref({
            location_id: null,
            date: null,
            burger_name: '',
            bun_rating: null,
            bun_remarks: '',
            patty_rating: null,
            patty_remarks: '',
            toppings_rating: null,
            toppings_remarks: '',
            fries_rating: null,
            fries_remarks: '',
            taste_total_rating: null,
            taste_total_remarks: '',
            location_rating: null,
            location_remarks: '',
            value_rating: null,
            value_remarks: '',
            x_factor_rating: null,
            x_factor_remarks: '',
            overall_rating: 0,
            overall_remarks: '',
        });
        var locations = ref([1, 2, 3]);

        onMounted(() => {
            fetchLocations();
        });

        const fetchBurgerReview = async (location_id) => {
            try {
                const response = await fetch(`/rest/burger_review/${location_id}`);
                const data = await response.json();
                if (data) {
                    formData.value['date'] = data['date'];
                    formData.value['burger_name'] = data['burger_name'];
                    formData.value['bun_rating'] = data['bun_rating'];
                    formData.value['bun_remarks'] = data['bun_remarks'];
                    formData.value['patty_rating'] = data['patty_rating'];
                    formData.value['patty_remarks'] = data['patty_remarks'];
                    formData.value['toppings_rating'] = data['toppings_rating'];
                    formData.value['toppings_remarks'] = data['toppings_remarks'];
                    formData.value['fries_rating'] = data['fries_rating'];
                    formData.value['fries_remarks'] = data['fries_remarks'];
                    formData.value['taste_total_rating'] = data['taste_total_rating'];
                    formData.value['taste_total_remarks'] = data['taste_total_remarks'];
                    formData.value['location_rating'] = data['location_rating'];
                    formData.value['location_remarks'] = data['location_remarks'];
                    formData.value['value_rating'] = data['value_rating'];
                    formData.value['value_remarks'] = data['value_remarks'];
                    formData.value['x_factor_rating'] = data['x_factor_rating'];
                    formData.value['x_factor_remarks'] = data['x_factor_remarks'];
                    formData.value['overall_remarks'] = data['overall_remarks'];
                    recalculateOverallRating();
                    }
                console.log('Fetched burger review:', formData);
            } catch (error) {
                console.error(error);
            }
        };

        const recalculateOverallRating = () => {
            formData.value['overall_rating'] = (formData.value['bun_rating'] +
                                                formData.value['patty_rating'] +
                                                formData.value['toppings_rating'] +
                                                formData.value['fries_rating'] +
                                                formData.value['taste_total_rating'] +
                                                formData.value['location_rating'] +
                                                formData.value['value_rating'] +
                                                formData.value['x_factor_rating']) / (7 + 1*(formData.value['fries_rating'] !== null));
        };

        const fetchLocations = async () => {
            try {
                const response = await fetch('/rest/burger_locations');
                const data = await response.json();
                if (data) {
                    locations.value = data;
                }
            } catch (error) {
                console.error(error);
            }
        };

        watch(
        () => formData.value.location_id, (newVal) => {
            if (newVal) {
                fetchBurgerReview(newVal);
                console.log('Fetching burger review for location_id:', newVal);
            }
        });
        watch(
        () => formData, (newVal) => {
            if (newVal) {
                recalculateOverallRating();
            }
        }, { deep: true }
    );

        return {
            formData,
            locations,
            fetchBurgerReview
        };
    }
});

app.mount('#app');