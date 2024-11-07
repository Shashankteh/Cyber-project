package web

import (
	"log/slog"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"

	"github.com/ShorterKing/Cyber-project/internal/check"
	"github.com/ShorterKing/Cyber-project/internal/conf"
	"github.com/ShorterKing/Cyber-project/internal/models"
)

func configHandler(c *gin.Context) {
	var guiData models.GuiData

	guiData.Config = appConfig

	guiData.Themes = []string{"cerulean", "cosmo", "cyborg", "darkly", "emerald", "flatly", "grass", "grayscale", "journal", "litera", "lumen", "lux", "materia", "minty", "morph", "ocean", "pulse", "quartz", "sand", "sandstone", "simplex", "sketchy", "slate", "solar", "spacelab", "superhero", "united", "vapor", "wood", "yeti", "zephyr"}

	file, err := pubFS.ReadFile("public/version")
	check.IfError(err)
	version := string(file)
	guiData.Version = version[8:]

	c.HTML(http.StatusOK, "header.html", guiData)
	c.HTML(http.StatusOK, "config.html", guiData)
}

func saveConfigHandler(c *gin.Context) {

	appConfig.Host = c.PostForm("host")
	appConfig.Port = c.PostForm("port")
	appConfig.Theme = c.PostForm("theme")
	appConfig.Color = c.PostForm("color")
	appConfig.NodePath = c.PostForm("node")
	appConfig.ShoutURL = c.PostForm("shout")

	conf.Write(appConfig)

	slog.Info("Writing new config to " + appConfig.ConfPath)

	c.Redirect(http.StatusFound, "/config")
}

func saveSettingsHandler(c *gin.Context) {

	appConfig.LogLevel = c.PostForm("log")
	appConfig.ArpArgs = c.PostForm("arpargs")
	appConfig.Ifaces = c.PostForm("ifaces")

	appConfig.UseDB = c.PostForm("usedb")
	appConfig.PGConnect = c.PostForm("pgconnect")

	timeout := c.PostForm("timeout")
	trimHist := c.PostForm("trim")
	appConfig.Timeout, _ = strconv.Atoi(timeout)
	appConfig.TrimHist, _ = strconv.Atoi(trimHist)

	histdb := c.PostForm("histdb")
	if histdb == "on" {
		appConfig.HistInDB = true
	} else {
		appConfig.HistInDB = false
	}

	conf.Write(appConfig)

	slog.Info("Writing new config to " + appConfig.ConfPath)

	updateRoutines() // routines-upd.go

	c.Redirect(http.StatusFound, "/config")
}

