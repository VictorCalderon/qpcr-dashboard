<template>
  <div>
    <div v-if="!accessToken">
      <modal-Login></modal-Login>
    </div>
    <div v-else>
      <modal-SearchDatabase></modal-SearchDatabase>
      <modal-AddExperimentData></modal-AddExperimentData>
      <modal-EditExperiment></modal-EditExperiment>
      <modal-ExportExperiment></modal-ExportExperiment>
      <Menu></Menu>

      <b-form-row class="mx-0">
        <b-col>
          <!-- <keep-alive> -->
          <router-view />
          <!-- </keep-alive> -->
        </b-col>
      </b-form-row>
    </div>
  </div>
</template>

<script>
import Menu from "@/components/navigation/Menu";
import AddExperimentData from "@/components/modals/AddExperimentData";
import SearchDatabase from "@/components/modals/SearchDatabase";
import EditExperiment from "@/components/modals/EditExperiment";
import ExportExperiment from "@/components/modals/ExportExperiment";
import Login from "@/components/modals/LoginModal";

export default {
  components: {
    Menu,
    "modal-AddExperimentData": AddExperimentData,
    "modal-SearchDatabase": SearchDatabase,
    "modal-Login": Login,
    "modal-EditExperiment": EditExperiment,
    "modal-ExportExperiment": ExportExperiment,
  },

  computed: {
    accessToken() {
      return this.$store.getters.accessToken;
    },

    currentExperiment() {
      return this.$store.getters.currentExperiment;
    },
  },

  methods: {
    startApp() {
      this.$store.dispatch("initExperiments");
      this.$store.dispatch("loadExperiments");
      this.$store.dispatch("getSampleLocationSchemas");
    },
  },

  watch: {
    accessToken() {
      if (this.accessToken != null) {
        this.startApp();
      }
    },
  },
};
</script>

<style lang="scss">
$GreyLight: #d8d8d8;
$GreyDark: #969696;
$GreenRef: #00843d;
$GreenRefDark: #005c2b;
$GreenRefLight: #01a34d;
$GreyDarker: #505050;
$GreyBackground: #e6e6e6;
$GreyBackgroundDark: #535353;
$Indicator: #539ee4;

body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

*:focus {
  outline: none !important;
  box-shadow: none !important;
}
</style>