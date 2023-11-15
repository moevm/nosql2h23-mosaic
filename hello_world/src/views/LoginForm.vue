<script setup>
import {ref} from 'vue';
import {useField, useForm} from 'vee-validate'
import axios from "axios";
import router from "../router/router";
// import {userAuthorized} from "../utils/utils";

const isLogin = ref(true);
const logInError = ref(false);
const signUpError = ref(false);
let userAuthorized = ref(false);

const { handleSubmit, handleReset } = useForm({
    validationSchema: {
        email (value) {
            if (/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(value)) return true

            return 'Введите e-mail правильно.'
        },
        password (value) {
            if (/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/.test(value)) return true

            return 'Пароль должен содержать минимум 1 заглавную букву, 1 строчную букву, 1 цифру, ' +
                '1 специальный символ. Длина не менее 8 символов.'
        },
    },
})
const email = useField('email')
const password = useField('password')

const userLogIn = async () => {
    const user = {
        email: email.value.value,
        password: password.value.value,
    }
    await axios
        .post(`http://localhost:5173/login`, user)
        .catch(() => {
            logInError.value = true
        })
        .then(async (res) => {
            // localStorage.setItem('token', res.data.token)
            localStorage.setItem('email', res.data.email)
            localStorage.setItem('password', res.data.password)

            userAuthorized.value = !userAuthorized.value

            await router.push('/')
        })
}

const userSignUp = handleSubmit(async () => {
    const user = {
        email: email.value.value,
        password: password.value.value,
    }
    await axios
        .post(`http://localhost:5173/authenticate`, user)
        .catch(() => {
            signUpError.value = true
        })
        .then(() => {
            if (signUpError.value === false) toggleForm();
        })
})

const toggleForm = () => {
    isLogin.value = !isLogin.value;
    logInError.value = false
    signUpError.value = false
};
</script>

<template>
<!--    <div class="alert-container">-->
<!--        <v-alert-->
<!--                closable-->
<!--                icon="mdi-alert-circle-outline"-->
<!--                variant="tonal"-->
<!--                color="error"-->
<!--                v-if="logInError || signUpError"-->
<!--        >-->
<!--            {{ logInError ? 'Неправильный e-mail или пароль' : 'Такой пользователь уже существует'}}-->
<!--        </v-alert>-->
<!--    </div>-->
    <div class="authorization-container">
        <v-card
                variant="flat"
                class="authorization-card"
        >
            <div
                    v-if="isLogin"
                    key="logInContainer"
            >
                <v-card-title>Sign in</v-card-title>

                <v-text-field
                        v-model="email.value.value"
                        label="e-mail"
                        variant="plain"
                />

                <v-text-field
                        v-model="password.value.value"
                        label="password"
                        variant="plain"
                        type="password"
                />

                    <v-btn
                            class="log_button"
                            variant="text"
                            @click="userLogIn()"
                    >
                        Log in
                    </v-btn>

            </div>
            <div
                    v-else
                    key="signUpContainer"
            >
                <form
                        @submit.prevent="userSignUp()"
                        class="form__signup"
                >
                    <v-card-title>Sign up to start create</v-card-title>

                    <v-text-field
                            class="email_input"
                            v-model="email.value.value"
                            :error-messages="email.errorMessage.value"
                            label="e-mail"
                            variant="plain"
                    />

                    <v-text-field
                            v-model="password.value.value"
                            :error-messages="password.errorMessage.value"
                            label="password"
                            variant="plain"
                    />

                    <v-card-actions class="card-down">
                        <v-btn
                                variant="text"
                                @click="userSignUp()"
                        >
                            <v-icon icon="mdi-check"/>
                            Sign up
                        </v-btn>
                    </v-card-actions>
                </form>
            </div>

            <div class="text-center">
<!--                <router-link tag="button" class="change-form-type" to="/signup" @click="toggleForm">No account? Sign up there</router-link>-->
                <button
                        @click="toggleForm"
                        class="change-form-type"

                >
                    {{ isLogin ? 'No account? Sign up there' : 'Cancel' }}
                </button>
            </div>

          <v-card-actions class="card-down2">
            <v-btn @click="handleReset; signUpError = false">
              Очистить
            </v-btn>
          </v-card-actions>
        </v-card>
    </div>
</template>

<style scoped lang="sass">

.authorization-container
    display: flex
    justify-content: center
    align-items: center
    height: 600px

.authorization-card
    background-color: rgba(255, 255, 255, 0.93)
    width: 80vw
    max-width: 520px
    height: 630px
    padding: 20px
    justify-content: center
    align-items: inherit
    display: flex
    flex-flow: column wrap
    margin-left: 350px
    border-radius: 20px


.v-text-field
    color: black
    padding: 0
    text-align: center
    width: 300px
    margin-left: 26px

.change-form-type
    background-color: rgba(255, 255, 255, 0)
    border: none
    color: #000acb
    padding: 15px 32px
    text-align: center
    text-decoration: none
    display: inline-block
    font-size: 16px

.v-card-title
    text-align: center
    text-decoration: none
    padding-bottom: 40px
    font-size: xx-large

.log_button
    background-color: rgba(39, 47, 92)
    color: white
    width: 300px
    height: 150px
    max-height: 150px
    margin-left: 26px
    flex-flow: column wrap

.reset_button
    background-color: rgba(255, 255, 255, 0)
    margin-top: 10px
    margin-left: 175px

</style>