<template>
  <div>
    <b-modal
      id="search-experiments-modal"
      ref="search-experiments-modal"
      class="text-center"
      button-size="sm"
      size="lg"
      scrollable
      header-bg-variant="dark"
      header-text-variant="light"
      title="Search qPCR Database"
      hide-footer
    >
      <b-tabs content-class="mt-3" fill>
        <b-tab title="Experiments" lazy>
          <b-container>
            <b-row class="pb-2 mx-1">
              <b-col>
                <div class="text-center">
                  <label for="input-experimentname">Type name</label>
                  <b-form-input
                    id="input-experimentname"
                    v-model="name"
                    class="text-center"
                    placeholder="Enter experiment name"
                  ></b-form-input>
                </div>
              </b-col>
              <b-col>
                <div class="text-center">
                  <label for="input-datepicker">Choose a date</label>
                  <b-form-input
                    id="input-datepicker"
                    v-model="date"
                    class="text-center"
                    placeholder="Format: YYYY-MM-DD"
                  ></b-form-input>
                </div>
              </b-col>
              <b-col>
                <div class="text-center">
                  <label for="input-method">Methodology</label>
                  <b-form-input
                    id="input-method"
                    v-model="methodology"
                    class="text-center"
                    locale="en"
                    placeholder="Enter method used"
                  ></b-form-input>
                </div>
              </b-col>
            </b-row>
            <b-row v-if="queriedExperiments.length > 0" class="border my-2 mx-1 rounded">
              <b-col>
                <b-table
                  :items="queriedExperiments"
                  :fields="experimentFields"
                  :tbody-tr-class="rowClass"
                  :busy="loadingResults"
                  hover
                  borderless
                  small
                  selectable
                  select-mode="single"
                  @row-selected="onExperimentSelected"
                  :per-page="perPage"
                  :current-page="currentPageExperiments"
                ></b-table>
              </b-col>
            </b-row>
            <b-row v-else align-h="center" class="border my-2 mx-1 rounded">
              <b-col>
                <div align-h="center">
                  <h5 class="my-5 text-center">Your search had no matches</h5>
                </div>
              </b-col>
            </b-row>
          </b-container>
          <hr />
          <b-container>
            <b-row align-h="start">
              <b-col>
                <b-pagination
                  v-model="currentPageExperiments"
                  :total-rows="experimentRows"
                  :per-page="perPage"
                  aria-controls="my-table"
                  id="paginator-experiments"
                  class="text-center"
                ></b-pagination>
              </b-col>
              <b-col cols="3"></b-col>
              <b-col>
                <b-button size="md" variant="info" @click="queryExperiments" class="mx-1">Search</b-button>
                <b-button
                  size="md"
                  variant="success"
                  @click="selectExperiment"
                  :disabled="activeOpenExperiment"
                  class="mx-1"
                >Open</b-button>
                <b-button size="md" variant="warning" @click="hideModal()" class="mx-1">Cancel</b-button>
              </b-col>
            </b-row>
          </b-container>
        </b-tab>
        <b-tab title="Samples" lazy>
          <b-container>
            <b-row class="pb-2 mx-1" align-h="center">
              <b-col cols="6">
                <div class="text-center">
                  <label for="input-samplename">Type name</label>
                  <b-form-input
                    id="input-samplename"
                    v-model="sample"
                    class="text-center"
                    placeholder="Enter sample name"
                  ></b-form-input>
                </div>
              </b-col>
            </b-row>

            <b-row v-if="queriedSamples.length > 0" class="border my-2 mx-1 rounded">
              <b-col>
                <b-table
                  :items="queriedSamples"
                  :fields="sampleFields"
                  :busy="loadingResults"
                  hover
                  borderless
                  small
                  selectable
                  select-mode="single"
                  @row-selected="onSampleSelected"
                  :per-page="perPage"
                  :current-page="currentPageSamples"
                ></b-table>
              </b-col>
            </b-row>
            <b-row
              v-if="searched && queriedSamples.length == 0"
              align-h="center"
              class="border my-2 mx-1 rounded"
            >
              <b-col>
                <div align-h="center">
                  <h5 class="my-5 text-center">Your search had no matches</h5>
                </div>
              </b-col>
            </b-row>
          </b-container>
          <hr />
          <b-row align-h="start">
            <b-col>
              <b-pagination
                v-model="currentPageSamples"
                :total-rows="sampleRows"
                :per-page="perPage"
                aria-controls="my-table"
                id="paginator-samples"
                class="text-center"
              ></b-pagination>
            </b-col>
            <b-col cols="3"></b-col>
            <b-col>
              <b-button size="md" variant="info" @click="querySamples" class="mx-1">Search</b-button>
              <b-button
                size="md"
                variant="success"
                @click="selectSample"
                :disabled="activeOpenSample"
                class="mx-1"
              >Open</b-button>
              <b-button size="md" variant="warning" @click="hideModal()" class="mx-1">Cancel</b-button>
            </b-col>
          </b-row>
        </b-tab>
      </b-tabs>
    </b-modal>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedExperiment: null,
      selectedSample: null,
      activeOpenExperiment: true,
      activeOpenSample: true,
      searched: false,
      loadingResults: false,
      perPage: 10,
      currentPageSamples: 1,
      currentPageExperiments: 1,
      experimentFields: [
        {
          key: "name",
          sortable: true
        },
        {
          key: "date",
          sortable: true
        },
        {
          key: "methodology",
          sortable: true
        },
        {
          key: "analyzed",
          sortable: true
        }
      ],
      sampleFields: [
        {
          key: "sample"
        },
        {
          key: "name",
          sortable: true
        },
        {
          key: "marker",
          sortable: true
        },
        {
          key: "amp_cq",
          sortable: true
        }
      ],
      date: null,
      name: null,
      analyzed: null,
      methodology: null,
      sample: null
    };
  },

  methods: {
    async queryExperiments() {
      const params = {
        name: this.name,
        date: this.date,
        analyzed: this.analyzed,
        methodology: this.methodology
      };
      this.loadingResults = true;
      await this.$store
        .dispatch("queryExperiments", params)
        .then((this.loadingResults = false));
    },

    async querySamples() {
      const params = {
        sample: this.sample
      };
      this.loadingResults = true;
      await this.$store.dispatch("querySamples", params).then(() => {
        this.searched = true;
        this.loadingResults = false;
      });
    },

    hideModal() {
      this.$refs["search-experiments-modal"].hide();
      this.searched = false;
    },

    onExperimentSelected(items) {
      this.selectedExperiment = items;
      this.activeOpenExperiment = false;
    },

    onSampleSelected(items) {
      this.selectedSample = items;
      this.activeOpenSample = false;
    },

    async selectExperiment() {
      if (this.selectExperiment) {
        await this.$store.dispatch(
          "selectExperiment",
          this.selectedExperiment[0]
        );
        await this.$store.dispatch("loadCurrentSamples");
        await this.$store.dispatch("loadExperimentFluorescences");
        await this.$store.dispatch("loadCurrentExperimentResults");
        this.selectedExperiment = null;
        this.hideModal();
      }
    },

    async selectSample() {
      if (this.selectSample) {
        await this.$store.dispatch("selectExperiment", this.selectedSample[0]);
        await this.$store.dispatch("loadCurrentSamples");
        await this.$store.dispatch("loadExperimentFluorescences");
        await this.$store.dispatch("loadCurrentExperimentResults");
        // await this.$store.dispatch(
        //   "filterSamples",
        //   this.selectedSample[0].sample
        // );
        this.selectedSample = null;
        this.hideModal();
      }
    },

    rowClass(item, type) {
      if (!item || type !== "row") return;
      if (item.analyzed === false) return "";
    }
  },

  computed: {
    queriedExperiments() {
      return this.$store.getters.queriedExperiments;
    },

    queriedSamples() {
      return this.$store.getters.queriedSamples;
    },

    sampleRows() {
      return this.queriedSamples.length;
    },

    experimentRows() {
      return this.queriedExperiments.length;
    }
  },

  mounted() {
    this.queryExperiments();
  }
};
</script>

<style>
</style>