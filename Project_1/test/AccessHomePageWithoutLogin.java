package Project;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;

import java.util.concurrent.TimeUnit;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

public class AccessHomePageWithoutLogin {
	 private WebDriver driver;
	 
	  private StringBuffer verificationErrors = new StringBuffer();

	  @Before
	  public void setUp() throws Exception {
	    driver = new FirefoxDriver();
	    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
	  }

	  @Test
	  public void testAccessHomePageWithoutLogin() throws Exception {
	    driver.get("http://127.0.0.1:5000/home");
	    assertEquals ("home", driver.getTitle()); 
	  }
	  
	  @Test
	  public void testAccessConstraintsPageWithoutLogin() throws Exception {
	    driver.get("http://127.0.0.1:5000/constraints");
	    assertEquals ("constraints", driver.getTitle());
	  }
	  
	  @Test
	  public void testAccessGaneratePageWithoutLogin() throws Exception {
	    driver.get("http://127.0.0.1:5000/generate");
	    assertEquals ("generate", driver.getTitle());
	  }
	  
	  @Test
	  public void testAccessViewPageWithoutLogin() throws Exception {
	    driver.get("http://127.0.0.1:5000/constraints");
	    assertEquals ("view", driver.getTitle());
	  }
	  

	  @After
	  public void tearDown() throws Exception {
	    driver.quit();
	    String verificationErrorString = verificationErrors.toString();
	    if (!"".equals(verificationErrorString)) {
	      fail(verificationErrorString);
	    }
	  }
}
