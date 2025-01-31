{{- define "helper.matchLabels" -}}
app.kubernetes.io/name: applicationmapper
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "helper.labels" -}}
{{- include "helper.matchLabels" . }}
app.kubernetes.io/version: "{{ default .Chart.AppVersion .Values.deployment.image.tag }}"
{{- end }}

{{- define "helper.webhook.baseUrl" -}}
{{- if .Values.controller.webhook.baseUrl -}}
{{ .Values.controller.webhook.baseUrl }}
{{- else -}}
{{- if not .Values.deployment.install -}}
{{ fail "Because `.deployment.install` is set to `false`, you must specify a `.controller.webhook.baseUrl`" }}
{{- end -}}
http://{{ .Release.Name }}.{{ .Release.Namespace }}.svc:8000
{{- end -}}
{{- end }}
