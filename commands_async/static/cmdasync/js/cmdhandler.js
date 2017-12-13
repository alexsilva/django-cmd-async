cmdasyncform = {
    csrfSafeMethod: function(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    },
    getCookie: function(name) {
      var start = document.cookie.indexOf(name + "=");
      var len = start + name.length + 1;
      if ((!start) && (name !== document.cookie.substring(0, name.length))) {
        return null;
      }
      if (start === -1) return null;
      var end = document.cookie.indexOf(';', len);
      if (end === -1) end = document.cookie.length;
      return document.cookie.substring(len, end);
    },

    init: function (outputelem) {
        this.$output = $(outputelem);
        this.update = true;
        this.running = false;
        this.events = {
            'form-valid': [],
            'update-finish': [],
            'updating': []
        };
        this.$form = null;
        this.task = null;
        this.requestTimeout = null;
    },
    request: function(task) {
        if (!this.running)
            this.update = true;
        var self = this;
        var req = $.ajax({
            type: "get",
            url: "status/" + task.id,
            cache: false
        });
        req.done(function (data) {
            var task = data.task;
            var $output = self.$output;
            self.exc_event_callbacks('updating', self.$form);
            if (self.update) {
                if (task.ready) {
                    if (!task.failed) {
                        $output.prepend(task.output)
                    } else {
                        $output.prepend(task.traceback)
                    }
                    $output.prepend("arguments(" + self.$form.serialize()  + ")\n");
                    $output.prepend("command(" + self.task.command.name  + ")\n");
                    $output.prepend("task-id(" + task.id + ")\n");
                    self.running = false;
                    self.exc_event_callbacks('update-finish', self.$form);
                } else {
                    // new update check
                    this.requestTimeout = setTimeout(function () {
                        self.running = true;
                        self.request(task)
                    }, 1000);
                }
            } else {
                self.running = false;
                self.exc_event_callbacks('update-finish', self.$form);
            }
        });
        req.fail(function () {
            self.running = false;
            self.exc_event_callbacks('update-finish', self.$form);
        });
    },
    revoke_task : function () {
        var self = this;
        var csrftoken = this.getCookie("csrftoken");
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: "status/" + self.task.id,
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
        if (this.requestTimeout !== null)
            clearTimeout(this.requestTimeout);
        this.update = !this.running;
    },

    add_event_callback: function(name, fn) {
        this.events[name].push(fn);
    },

    on_form_valid : function (data) {
        this.task = data.task;
        this.request(this.task);
    },

    exc_event_callbacks: function(name) {
        var event_callbacks = this.events[name];
        var length = event_callbacks.length;
            for (var i=0; i < length; i++) {
                event_callbacks[i].apply(this, Array.prototype.slice.call(arguments, 1));
            }
    },
    ajax: function (elem, options) {
        var self = this;
        options = options || {};
        options.dataType = 'json';

        if (this.events['form-valid'].indexOf(this.on_form_valid) === -1)
            this.add_event_callback("form-valid", this.on_form_valid.bind(this));

        options.success = function(responseText, statusText, xhr, $form) {
            self.exc_event_callbacks('form-valid', responseText, statusText, xhr, $form);
        };
        this.$form = $(elem).ajaxForm(options);
        return options;
    }
};
