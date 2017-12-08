cmdayncform = {
    csrfSafeMethod: function(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    },
    init: function (outputelem) {
        this.$output = $(outputelem);
        this.update = true;
        this.running = false;
        this.successAjaxArr = [];
        this.onUpdateFinishArr = [];
        this.$form = null;
        this.taskid = null;
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
                self.running = false;
                self.exc_fnarr(self.onUpdateFinishArr, self.$form);
            } else if (self.update) {
                // new update check
                setTimeout(function () {
                    self.running = true;
                    self.request(task_id)
                }, 1000);
            } else {
                self.running = false;
                self.exc_fnarr(self.onUpdateFinishArr, self.$form);
            }
        });
        req.fail(function () {

        });
    },
    revoke_task : function () {
        var self = this;
        var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: "status/" + this.taskid,
            beforeSend: function(xhr, settings) {
                if (!self.csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function(data) {
                if (!data.status) alert(data.error);
            }
        })
    },
    clear_output: function () {
      this.$output.empty();
    },

    update_abort: function () {
        this.update = !this.running;
    },

    add_ajax_success : function(fn) {
        this.successAjaxArr.push(fn);
    },

    add_ajax_update_finish : function(fn) {
        this.onUpdateFinishArr.push(fn);
    },

    on_ajax_success : function (data) {
        var task = data.task;
        this.taskid = task.id;
        this.request(task.id);
    },

    exc_fnarr: function(fnarr) {
        var length = fnarr.length;
            for (var i=0; i < length; i++) {
                fnarr[i].apply(this, Array.prototype.slice.call(arguments, 1));
            }
    },
    ajax: function (elem, options) {
        var self = this;
        options = options || {};
        options.dataType = 'json';

        if (this.successAjaxArr.indexOf(this.on_ajax_success) === -1)
            this.add_ajax_success(this.on_ajax_success.bind(this));

        options.success = function(responseText, statusText, xhr, $form) {
            self.exc_fnarr(self.successAjaxArr, responseText, statusText, xhr, $form);
        };
        this.$form = $(elem).ajaxForm(options);
        return options;
    }
};
