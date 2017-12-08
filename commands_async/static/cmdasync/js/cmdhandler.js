cmdaync = {
    init: function (outputelem) {
        this.$output = $(outputelem);
        this.update = true;
        this.running = false;
    },
    request: function(task_id) {
        if (!this.running)
            this.update = true;
        var self = this;
        var req = $.ajax({
            type: "get",
            url: "status/" + task_id,
            cache: false
        });
        req.success(function (data) {
            var task = data.task;
            var $output = self.$output;
            if (task.ready) {
                $output.append("TaskID(" + task.id + ")\n");
                if (!task.failed) {
                    $output.append(task.output)
                } else {
                    $output.append(task.traceback)
                }
            } else if (self.update) {
                // new update check
                self.running = true;
                setTimeout(function () {
                    self.request(task_id)
                }, 1000);
            } else {
                self.running = false;
            }
        });
        req.fail(function () {

        });
    },
    clear_output: function () {
      this.$output.empty();
    },
    update_abort: function () {
        this.update = false;
    },
    ajaxform: function (elem) {
        var self = this;
        $(elem).ajaxForm({
            success: function (data) {
                var task = data.task;
                self.request(task.id);
            }
        });
    }
};
