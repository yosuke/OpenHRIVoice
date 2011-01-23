<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="text" encoding="utf-8" />

  <xsl:template match="data">
    <xsl:value-of select="@text"/>
  </xsl:template> 

</xsl:stylesheet>
